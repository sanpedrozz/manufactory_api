from sqlalchemy import func
from pydantic import ValidationError
from time import sleep

from app.storage.warehouse_robots import RobotsController, TasksController
from database import Session
from schema import RobotBaseModel, TaskBaseModel
from logs.logger import logger
from app.service.plc_client import PLCClient
from snap7.util import get_uint, get_usint, set_uint, set_usint, set_string, get_string
from settings import plc_settings, general_settings
from database.models import TasksBase


class TaskHandler:
    def __init__(self, session: Session, ip):
        self.plc_client = PLCClient(ip)
        self.store_tasks = StoreTasks(session)
        self.message_wait_status_start_task = False  # Атрибут сообщения об ожидании старта робота

    def get_task_status(self, offset):
        data = self.plc_client.read_data(plc_settings.TASK_DB,
                                         plc_settings.TASK_LENGTH * offset + plc_settings.TASK_STATUS_OFFSET, 2)
        task_status = get_uint(data, 0)
        return task_status

    def get_task_id(self, offset):
        data = self.plc_client.read_data(plc_settings.TASK_DB,
                                         plc_settings.TASK_LENGTH * offset + plc_settings.TASK_ID_OFFSET, 38)
        return {
            "task_id": get_string(data, 0)
        }

    def get_task_moving(self, offset):
        data = self.plc_client.read_data(plc_settings.TASK_DB,
                                         plc_settings.TASK_LENGTH * offset + plc_settings.TASK_MOVING_OFFSET, 6)
        return {
            'zone_out': get_uint(data, 0),
            'zone_in': get_uint(data, 2),
            'qty': get_uint(data, 4)
        }

    def get_task_sheet(self, qty, offset):
        task_sheet = {
            'cover': [],
            'depth': []
        }
        data = self.plc_client.read_data(plc_settings.TASK_DB,
                                         plc_settings.TASK_LENGTH * offset + plc_settings.TASK_SHEET_OFFSET, 400)
        for i in range(qty):
            task_sheet['cover'].append(get_usint(data, i * 2))
            task_sheet['depth'].append(get_usint(data, i * 2 + 1))
        return task_sheet

    def get_task_from_plc(self, offset):
        moving = self.get_task_moving(offset)
        sheet = self.get_task_sheet(moving['qty'], offset)
        task_id = self.get_task_id(offset)
        return {**task_id, **moving, **sheet}

    def get_current_qty(self, offset):
        data = self.plc_client.read_data(plc_settings.STATUS_DB,
                                         plc_settings.STATUS_LENGTH * offset + plc_settings.TASK_QTY_OFFSET, 2)
        current_qty = get_uint(data, 0)
        return current_qty

    def set_task_status(self, status, offset):
        data_task_status = bytearray(2)
        set_uint(data_task_status, 0, int(status))
        self.plc_client.write_data(plc_settings.TASK_DB,
                                   plc_settings.TASK_LENGTH * offset + plc_settings.TASK_STATUS_OFFSET, data_task_status)

    def set_task_id(self, task: TaskBaseModel, offset):
        data_task_id = bytearray(38)
        set_string(data_task_id, 0, task.task, 38)
        self.plc_client.write_data(plc_settings.TASK_DB,
                                   plc_settings.TASK_LENGTH * offset + plc_settings.TASK_ID_OFFSET, data_task_id)
        return {
            "task_id": task.task
        }

    def set_task_moving(self, task: TaskBaseModel, offset):
        data_moving = bytearray(2)
        set_uint(data_moving, 0, task.zone_out)
        set_uint(data_moving, 2, task.zone_in)
        set_uint(data_moving, 4, task.qty)
        self.plc_client.write_data(plc_settings.TASK_DB,
                                   plc_settings.TASK_LENGTH * offset + plc_settings.TASK_MOVING_OFFSET, data_moving)
        return {
            'zone_out': task.zone_out,
            'zone_in': task.zone_in,
            'qty': task.qty
        }

    def set_task_sheet(self, task: TaskBaseModel, offset):
        data_sheet = bytearray(400)
        task_sheet = {
            'cover': [],
            'depth': []
        }
        for i in range(task.qty):
            set_usint(data_sheet, i * 2, task.cover)
            set_usint(data_sheet, i * 2 + 1, task.depth)
            task_sheet['cover'].append(task.cover)
            task_sheet['depth'].append(task.depth)
        self.plc_client.write_data(plc_settings.TASK_DB,
                                   plc_settings.TASK_LENGTH * offset + plc_settings.TASK_SHEET_OFFSET, data_sheet)
        return task_sheet

    def set_task_to_plc(self, task: TaskBaseModel, offset):
        moving = self.set_task_moving(task, offset)
        sheet = self.set_task_sheet(task, offset)
        task_id = self.set_task_id(task, offset)
        return {**task_id, **moving, **sheet}

    def post_task(self, task: TaskBaseModel, offset):
        set_task = self.set_task_to_plc(task, offset)
        sleep(0.1)
        get_task = self.get_task_from_plc(offset)
        if set_task == get_task:
            logger.info(f"Задание в PLC отправлено корректно")
            return True
        else:
            logger.info(f"Задание в PLC отправлено НЕ корректно")
            return False

    def post_start(self, task: TaskBaseModel, offset):
        # Проверяем, записан ли старт ext
        if task.stage_plc == 0 or task.stage_plc == 3:
            self.set_task_status(1, offset)
            logger.info(f"Робот {task.name}: {task.stage_plc} - Готов к старту задания. Отправлена команда на запуск")

    def working(self, task: TaskBaseModel, offset):
        # Шаг 0: Подготавливаем данные
        task.stage_plc = self.get_task_status(offset)

        # Шаг 1: Отправляем, что OPC получило задание
        if task.stage_db == 0:
            if task.stage_plc == 0 or task.stage_plc == 3:
                if self.store_tasks.update_stage_task_by_task(task, 1):
                    task.stage_db = 1
                    logger.info(f"{task.name}: {task.task} - Задание Сконфигурировано")
                else:
                    logger.info(f"{task.name}: {task.task} - Задание НЕ Сконфигурировано")

        # Шаг 2: Отравляем задание в PLC
        if task.stage_db == 1:
            if task.stage_plc == 0 or task.stage_plc == 3:
                if self.post_task(task, offset):
                    self.post_start(task, offset)
                    logger.info(f"Робот {task.name}. Статус {task.stage_plc}: Задание отправлено")
                    self.message_wait_status_start_task = False
            elif task.stage_plc == 1 and self.message_wait_status_start_task == True:
                logger.info(f"Робот {task.name}. Статус {task.stage_plc}: Робот ожидает начала выполнения задания")
                self.message_wait_status_start_task = True
            elif task.stage_plc == 2:
                self.store_tasks.update_stage_task_by_task(task, 2)
                self.store_tasks.update_dstart_task_by_task(task)
                task.stage_db = 2
                logger.info(f"Робот {task.name}. Статус {task.stage_plc}: Робот начал Перекладку")

        # Шаг 3: Ждем завершения работы программы
        if task.stage_db == 2:
            task.qty_cur = self.get_current_qty(offset)
            if task.stage_plc == 0 or task.stage_plc == 3:
                self.store_tasks.update_qty_task_by_task(task, task.qty_cur)
                self.store_tasks.update_status_task_by_task(task, 1)
                self.store_tasks.update_stage_task_by_task(task, 3)
                self.store_tasks.update_dfinish_task_by_task(task)
                logger.info(f"Робот {task.name}. Статус {task.stage_plc}:Задание Завершено")
                task = self.store_tasks.get_task_by_name(task.name)

            elif task.stage_plc == 1:
                logger.warning(f"Робот {task.name}. Ошибка логики работы! "
                               f"stage_db = {task.stage_db}, stage_plc = {task.stage_plc}")

            elif task.stage_plc == 2:
                if task.qty_cur > 0 and task.qty_cur != task.qty_old_cur:
                    task.qty_old_cur = task.qty_cur
                    self.store_tasks.update_qty_task_by_task(task, task.qty_cur)

                    logger.info(f"Робот {task.name}: переложил {task.qty_cur} из {task.qty}")

        return task

    def work_init(self, name, offset):
        logger.info(f"{'*' * 100}")

        logger.info(f"Робот {name} - Инициализация работы")

        stage_plc = int(self.get_task_status(offset))
        task_id = self.get_task_id(offset)

        if stage_plc == 0 or stage_plc == 3:
            task = self.store_tasks.get_task_by_name(name)

            if task == '' or task is None:
                logger.info(f"Робот {name} - Робот ожидает новое задание")
            else:
                logger.info(f"Робот {name} - Получил задание {task.task}")

        if stage_plc == 1:
            task = self.store_tasks.get_task_by_id(task_id['task_id'])
            qty = self.get_current_qty(offset)
            task.qty_cur = qty
            task.qty_old_cur = qty
            task.stage_plc = stage_plc
            logger.info(f"Робот {name} - Робот получил задание {task_id['task_id']}")

        if stage_plc == 2:
            task = self.store_tasks.get_task_by_id(task_id['task_id'])
            qty = self.get_current_qty(offset)
            task.qty_cur = qty
            task.qty_old_cur = qty
            task.stage_plc = stage_plc
            logger.info(f"Робот {name} - Робот выполняет задание {task_id['task_id']}")

        logger.info(f"{'*' * 100}")
        return task


class StoreRobots:
    def __init__(self, session: Session):
        # Инициализация экземпляра RfidOnRobotsController с переданной сессией базы данных
        self.robots_controller = RobotsController(session)

    def get_robots_by_active(self, active):
        """
        Получает данные о роботах и ПЛК из базы данных
        :param active: int - Значение активности
        :return: Dict[str, List[RobotBaseModel]] - Словарь, где ключи - IP-адреса ПЛК, а значениями - списки роботов
        """
        logger.info(f"{'*' * 100}")
        logger.info(f"Получение данных о Роботах и ПЛК из базы данных")

        robots_list = self._get_robots_list(active)
        plcs_list = self._get_plcs_list(robots_list)
        self._log_result(robots_list, plcs_list)

        logger.info(f"Данные о Роботах и ПЛК из базы данных - получены")
        logger.info(f"{'*' * 100}")

        return plcs_list

    def _get_robots_list(self, active):
        """
        Получает список роботов из базы данных по указанной активности.
        :param active: Int - Значение активности
        :return: List[RobotBaseModel] - Список объектов модели RobotBaseModel
        """
        robots_list = []
        robots = self.robots_controller.get_robots_by_active(active)
        for robot in robots:
            robots_list.append(
                RobotBaseModel(
                    name=robot.name,
                    ip=robot.ip_address,
                    n_robot=robot.n_robot-1
                )
            )
        return robots_list

    @staticmethod
    def _get_plcs_list(robots_list: list[RobotBaseModel]):
        """
        Группирует роботов по IP-адресу и возвращает словарь, где ключами - IP-адреса, а значениями - списки роботов.
        :param robots_list: List[RobotBaseModel] - Список объектов модели RobotBaseModel
        :return: Dict[str, List[RobotBaseModel]] - Словарь, где ключи - IP-адреса, а значениями - списки роботов
        """
        plcs_list = {}
        for robot in robots_list:
            if robot.ip not in plcs_list:
                plcs_list[robot.ip] = []
            plcs_list[robot.ip].append(robot)

        return plcs_list

    @staticmethod
    def _log_result(robots_list, plcs_list):
        logger.info(f"Найдено роботов: {len(robots_list)}")
        for robot in robots_list:
            logger.info(f"name: {robot.name}, ip: {robot.ip}, порядковый номер: {robot.n_robot + 1}")
        logger.info(f"Найдено ПЛК: {len(plcs_list)}")
        for plc in plcs_list:
            logger.info(f"ip: {plc}")


class StoreTasks:
    def __init__(self, session: Session):
        # Инициализация экземпляра RfidOnRobotsController с переданной сессией базы данных
        self.tasks_controller = TasksController(session)

    def get_task_by_name(self, name):
        """
        Получает следующие задачи по имени робота.
        :param name: Str - Имя робота
        :return: TaskBaseModel - Объект модели TaskBaseModel, представляющий следующую задачу по имени робота
        """
        try:
            task = self.tasks_controller.get_task_by_name(name)
            first_row = task.first()
            if first_row is not None:
                return TaskBaseModel(
                    name=name,
                    task=first_row.task,
                    zone_out=self._change_zone(name, first_row.zone_out),
                    zone_in=self._change_zone(name, first_row.zone_in),
                    qty=first_row.qty,
                    qty_cur=0,
                    qty_old_cur=0,
                    cover=first_row.cover,
                    depth=first_row.depth,
                    status=first_row.status,
                    stage_db=first_row.stage,
                    stage_plc=0
                )
            else:
                return self.get_empty_task(name)
        except ValidationError as e:
            error_messages = e.errors()
            error_fields = [error["loc"][0] for error in error_messages]
            if "zone_out" in error_fields:
                logger.warning(f"Ошибка в поле zone_out: Недопустимое значение")
            elif "zone_in" in error_fields:
                logger.warning(f"Ошибка в поле zone_in: Недопустимое значение")
            else:
                logger.warning(f"Произошла ошибка при валидации данных")
            return None

    def get_task_by_id(self, task_id):
        """
        Получает следующие задачи по имени робота.
        :param task_id: str - ID задания
        :return: TaskBaseModel - Объект модели TaskBaseModel, представляющий следующую задачу по имени робота
        """
        try:
            task = self.tasks_controller.get_task_by_id(task_id)
            first_row = task.first()
            if first_row is not None:
                return TaskBaseModel(
                    name=first_row.device,
                    task=first_row.task,
                    zone_out=self._change_zone(first_row.device, first_row.zone_out),
                    zone_in=self._change_zone(first_row.device, first_row.zone_in),
                    qty=first_row.qty,
                    qty_cur=0,
                    qty_old_cur=0,
                    cover=first_row.cover,
                    depth=first_row.depth,
                    status=first_row.status,
                    stage_db=first_row.stage,
                    stage_plc=0
                )
            else:
                return self.get_empty_task(task_id)
        except ValidationError as e:
            error_messages = e.errors()
            error_fields = [error["loc"][0] for error in error_messages]
            if "zone_out" in error_fields:
                logger.warning(f"Ошибка в поле zone_out: Недопустимое значение")
            elif "zone_in" in error_fields:
                logger.warning(f"Ошибка в поле zone_in: Недопустимое значение")
            else:
                logger.warning(f"Произошла ошибка при валидации данных")
            return None

    def update_stage_task_by_task(self, task: TaskBaseModel, stage: int):
        """
        Обновляет значение стадии задачи
        :param task: TaskBaseModel - Объект модели TaskBaseModel, представляющий задачу
        :param stage: int - Значение стадии задачи
        :return:
        """
        self.tasks_controller.update_value_by_task(task, stage=stage)
        return True

    def update_status_task_by_task(self, task: TaskBaseModel, status: int):
        """
        Обновляет значение статуса задачи
        :param task: TaskBaseModel - Объект модели TaskBaseModel, представляющий задачу
        :param status: int - Значение статуса задачи
        :return:
        """
        self.tasks_controller.update_value_by_task(task, status=status)

    def update_qty_task_by_task(self, task: TaskBaseModel, qty: int):
        """
        Обновляет значение количества переложенных листов
        :param task: TaskBaseModel - Объект модели TaskBaseModel, представляющий задачу
        :param qty: int - Значение количества задачи
        :return:
        """
        self.tasks_controller.update_value_by_task(task, qtyfact=qty)

    def update_dstart_task_by_task(self, task: TaskBaseModel):
        """
        Обновляет значение даты начала задачи на текущую дату и время
        :param task: TaskBaseModel - Объект модели TaskBaseModel, представляющий задачу
        :return:
        """
        self.tasks_controller.update_value_by_task(task, dstart=func.now())

    def update_dfinish_task_by_task(self, task: TaskBaseModel):
        """
        Обновляет значение даты завершения задачи на текущую дату и время
        :param task: TaskBaseModel - Объект модели TaskBaseModel, представляющий задачу
        :return:
        """
        self.tasks_controller.update_value_by_task(task, dfinish=func.now())

    @staticmethod
    def get_empty_task(name: str):
        return TaskBaseModel(
            name=name,
            task='',
            zone_out=0,
            zone_in=0,
            qty=0,
            qty_cur=0,
            qty_old_cur=0,
            cover=0,
            depth=0,
            status=0,
            stage_db=0,
            stage_plc=0
        )

    @staticmethod
    def _change_zone(name, zone):
        if int(name[-1]) in [1, 3]:
            zone_mapping = {
                1: 2,
                2: 3,
                3: None,
                4: 1,
                5: 4,
                6: None
            }
        else:
            zone_mapping = {
                1: None,
                2: 3,
                3: 2,
                4: None,
                5: 4,
                6: 1
            }
        if zone in zone_mapping:
            return zone_mapping.get(zone)

    def add_task(self, tasks):
        bad_task = any(
            (task['zone_in'], task['zone_out']) in general_settings.BAD_ZONE_PAIRS for task in tasks)

        for task in tasks:
            task_base = TasksBase(
                task=task['task'],
                pid=task['pid'],
                i=task['i'],
                device=task['device'],
                cell=task['cell'],
                zone_out=task['zone_out'],
                zone_in=task['zone_in'],
                qty=task['qty'],
                dcreate=task['dcreate'],
                cover=task['cover'],
                employee=task['employee'],
                depth=task['depth'],
                status=(2 if bad_task else 0),
                stage=0
            )
            self.tasks_controller.add_task(task_base)

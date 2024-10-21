import socket
from datetime import datetime
from enum import Enum

from src.api.printer.schemas import PrintData
from src.api.printer.zpl_class import ZPLLabel


class ItemsTextureEnum(Enum):
    LONG_SIDE = "LONG_SIDE"
    SHORT_SIDE = "SHORT_SIDE"
    WITHOUT_TEXTURE = "WITHOUT_TEXTURE"


async def print_label_service():
    # Пример данных для этикетки (или они могут поступать из другого источника)
    data = PrintData(
        label_id=425453007000009,
        length=807.0,
        width=727.0,
        thickness=3.0,
        cover='101 PE',
        size='807.0x727.0x3.0',
        count='7(9)',
        order='25453',
        client_pos='',
        site='www.expo-torg.ru',
        comment_lines=['', ''],
        comment='',
        l1={'val': 0.0, 'parent': False, 'thickness': 2},
        l2={'val': 0.0, 'parent': False, 'thickness': 2},
        w3={'val': 0.0, 'parent': False, 'thickness': 2},
        w4={'val': 0.0, 'parent': False, 'thickness': 2},
        l1_other_color='',
        l2_other_color='',
        w3_other_color='',
        w4_other_color='',
        curve=0,
        edge_dop='',
        texture='WITHOUT_TEXTURE',
        operations_info=''
    ).dict()

    # Подготовка сообщения
    prepared_message = prepare_message(data)

    # Отправка на принтер
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.connect(('192.168.23.134', 9100))  # IP и порт принтера
    mysocket.send(prepared_message.encode("utf-8"))
    mysocket.close()


def prepare_message(data: dict, is_reprint=True, x_offset=2, y_offset=0) -> str:  # noqa: C901, PLR0912, PLR0915
    # Размер этикетки в Ш*Д мм
    label = ZPLLabel(40, 60, printer_settings={"x_offset": x_offset, "y_offset": y_offset})

    # РАЗМЕРЫ ДЕТАЛИ
    # Размер детали по длине (сторона l1)
    label.add_text(x=9, y=1.67, text=data["length"], char_width=1.25, char_height=1.25, font="F")

    # Размер детали по ширине (сторона w4)
    label.add_text(
        x=33.75,
        y=2.84,
        text=data["width"],
        char_width=1.25,
        char_height=1.25,
        font="F",
        orientation="R",
    )

    # КРОМКИ
    if data["l1"]["val"] or data["curve"]:
        reverse = False
        if data["l1"]["parent"]:
            reverse = True
        # Рамка для размера по длине (сторона l1) - прямолинейное кромление
        label.add_box(
            x=17.75,
            y=0.84,
            width=75,
            height=40,
            thickness=data["l1"]["thickness"],
            rounding=data["curve"],
        )

        # Толщина кромки по длине (сторона l1)
        label.add_text(
            x=19,
            y=1,
            text=data["l1"]["val"],
            char_width=1.25,
            char_height=1.25,
            font="S",
            reverse=reverse,
        )
        if data["l1_other_color"]:
            label.add_text(
                x=25,
                y=1,
                text=data["l1_other_color"],
                char_width=1.4,
                char_height=1.8,
                font="0",
                reverse=reverse,
            )

    if data["l2"]["val"] or data["curve"]:
        reverse = False
        if data["l2"]["parent"]:
            reverse = True
        # Рамка для размера по длине (сторона l2) - прямолинейное кромление
        label.add_box(
            x=21.25,
            y=21.67,
            width=75,
            height=40,
            thickness=data["l2"]["thickness"],
            rounding=data["curve"],
        )

        # Толщина кромки по длине (сторона l2)
        label.add_text(
            x=22.67,
            y=21.84,
            text=data["l2"]["val"],
            char_width=1.25,
            char_height=1.25,
            font="S",
            reverse=reverse,
        )
        if data["l2_other_color"]:
            label.add_text(
                x=12,
                y=21.94,
                text=data["l2_other_color"],
                char_width=1.4,
                char_height=1.8,
                font="0",
                reverse=reverse,
            )

    if data["w3"]["val"] or data["curve"]:
        reverse = False
        if data["w3"]["parent"]:
            reverse = True
        # Рамка для размера по ширине (сторона w3) - прямолинейное кромление
        label.add_box(
            x=0.09,
            y=14.59,
            width=40,
            height=75,
            thickness=data["w3"]["thickness"],
            rounding=data["curve"],
        )

        # Толщина кромки по длине (сторона w3)
        label.add_text(
            x=0,
            y=15.59,
            text=data["w3"]["val"],
            char_width=1.25,
            char_height=1.25,
            font="S",
            orientation="R",
            reverse=reverse,
        )
        if data["w3_other_color"]:
            label.add_text(
                x=0,
                y=4.5,
                text=data["w3_other_color"],
                char_width=1.4,
                char_height=1.8,
                font="0",
                orientation="R",
                reverse=reverse,
            )

    if data["w4"]["val"] or data["curve"]:
        reverse = False
        if data["w4"]["parent"]:
            reverse = True
        # Рамка для размера по ширине (сторона w4) - прямолинейное кромление
        label.add_box(
            x=33.34,
            y=10.5,
            width=40,
            height=71,
            thickness=data["w4"]["thickness"],
            rounding=data["curve"],
        )

        # Толщина кромки по длине (сторона w4)
        label.add_text(
            x=33.17,
            y=11.54,
            text=data["w4"]["val"],
            char_width=1.25,
            char_height=1.25,
            font="S",
            orientation="R",
            reverse=reverse,
        )
        if data["w4_other_color"]:
            label.add_text(
                x=34.7,
                y=17,
                text=data["w4_other_color"],
                char_width=1.4,
                char_height=1.8,
                font="0",
                orientation="R",
                reverse=reverse,
            )

    # ИНФОРМАЦИЯ О ДЕТАЛИ
    # Декор детали + структура
    label.add_text(
        x=21.25,
        y=6.25,
        text=data["cover"],
        char_width=2.09,
        char_height=2.09,
        font="0",
    )

    # QR-код с ID детали
    label.add_qr(
        x=20.42,
        y=7.92,
        code=data["label_id"],
        error_correction="H",
        magnification=7,
    )

    # Номер заказа
    label.add_text(x=3.34, y=3.6, text=data["order"], char_width=1.15, char_height=1.25, font="S")

    # Позиция клиента
    label.add_text(
        x=3.34,
        y=6.67,
        text=data["client_pos"],
        char_width=2,
        char_height=2,
        font="0",
        change_international_font=28,
    )

    # Размеры детали
    label.add_text(x=3.34, y=9.15, text=data["size"], char_width=1.67, char_height=2.92, font="0")

    # Знак кромки не в цвет
    label.add_text(x=16.67, y=5.84, text=data["edge_dop"], char_width=3.5, char_height=5, font="B")

    # Наш номер детали (сквозной счетчик)
    label.add_text(x=27.92, y=21.67, text=data["count"], char_width=2, char_height=2.92, font="0")

    # Направление текстуры
    if data["texture"] and data["texture"] != ItemsTextureEnum.WITHOUT_TEXTURE:
        label.add_text(
            x=0,
            y=0.84,
            text="_7E",
            char_width=6 if data["texture"] == ItemsTextureEnum.SHORT_SIDE else 4,
            char_height=4 if data["texture"] == ItemsTextureEnum.SHORT_SIDE else 6,
            font="0",
            orientation="R" if data["texture"] == ItemsTextureEnum.SHORT_SIDE else "N",
        )

    # БЛОК ОПЕРАЦИЙ
    # Рамка в случае наличия operations_info
    if data["operations_info"]:
        label.add_box(x=0, y=11.67, width=240, height=38, thickness=0, color="W")
        label.add_text(
            x=0.17,
            y=12,
            text=data["operations_info"],
            char_width=1.8,
            char_height=3,
            font="0",
            change_international_font=28,
        )

    # Рамка для комментария
    label.add_box(x=3.75, y=14.59, width=195, height=80, thickness=3)

    # Однострочный комментарий
    if data["comment"]:
        if len(data["comment"]) == 1:
            label.add_text(
                x=10,
                y=15.3,
                text=data["comment"],
                char_width=7.5,
                char_height=7.5,
                change_international_font=28,
                font="0",
            )
        else:
            label.add_text(
                x=7,
                y=15.3,
                text=data["comment"],
                char_width=7.5,
                char_height=7.5,
                change_international_font=28,
                font="0",
            )
    else:
        # Первая строка комментария
        label.add_text(
            x=4.17,
            y=15.54,
            text=data["comment_lines"][0],
            char_width=2,
            char_height=2.4,
            font="0",
            change_international_font=28,
        )

        # Вторая строка комментария
        label.add_text(
            x=4.17,
            y=18.3,
            text=data["comment_lines"][1],
            char_width=2,
            char_height=2.4,
            font="0",
            change_international_font=28,
        )

    # ДАТА И ВРЕМЯ
    if is_reprint:
        # Дата перепечати
        now = datetime.now()
        label.add_text(
            x=0.84,
            y=21.67,
            text=datetime.strftime(now, "%d-%m-%Y"),
            char_width=1.4,
            char_height=1.4,
            font="0",
        )

        # Время перепечати
        label.add_text(
            x=0.84,
            y=23.34,
            text=datetime.strftime(now, "%H:%M:%S"),
            char_width=1.4,
            char_height=1.4,
            font="0",
        )

    return label.dumpZPL().replace("^FD_7E", "^FH_^FD_7E")


if __name__ == "__main__":
    import asyncio

    asyncio.run(print_label_service())

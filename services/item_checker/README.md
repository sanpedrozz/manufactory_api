project/
├── services/
│   ├── item_checker_service/
│   │   ├── src/
│   │   │   ├── app.py                       # Основной файл FastAPI
│   │   │   ├── routers/
│   │   │   │   └── view.py                 # Роут для отображения таблицы
│   │   │   └── templates/                  # Шаблоны HTML
│   │   │       ├── form.html               # Форма для ввода label_ids
│   │   │       └── table.html              # Таблица для отображения результатов
│   │   │   └── static/                     # Шаблоны HTML
│   │   │       └── styles.css              # Таблица для отображения результатов
│   │   ├── Dockerfile                      # Dockerfile для фронтенд-сервиса
│   │   ├── poetry.lock
│   │   ├── pyproject.toml
├── │   └── README.md

├── shared/
│   └── db/
│   │   ├── industrial_stg/
│   │   │   ├── database.py                 # Подключение к базе данных industrial_stg
│   │   │   ├── models.py                   # Модели базы данных
│   │   │   ├── base.py                     # ХЗ понадобится или нет, т.к. из этой базы только читаем
│   └── config/
│   │   ├── config.py

├── docker-compose.yml
└── README.md
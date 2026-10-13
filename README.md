# Airflow ISS Homework


**Автор:** [Михаил Батаев](https://github.com/rodionmirov)  
**Курс:** OTUS Data Engineer  
**Тема:** Apache Airflow. Сложные пайплайны. Подготовка и установка на расписание DAG выгрузки данных из источников.
=======
Домашнее задание: пайплайн сбора координат МКС (ISS) с помощью Apache Airflow и PostgreSQL.

## Структура проекта

```
airflow-iss-homework/
├── dags/
│   └── iss_pipeline.py       # Код DAG (TaskFlow API, Python)
├── sql/
│   └── init.sql              # скрипт создания таблицы при старте БД
├── screenshots/
│  └── *.jpg # Скриншоты выполнения домашнего задания
│   
├── docker-compose.yaml       # Описание инфраструктуры (8 контейнеров)
├── .env                      # Переменные окружения
├── README.md                 
```


## Этап 1. Клонирование и запуск стенда

```bash
git clone https://github.com/rodionmirov/airflow-iss-homework.git
cd airflow-iss-homework
mkdir -p logs
=======
```

Создать папку логов:

```bash
mkdir logs
```

Инициализировать Airflow:

```bash
docker compose up airflow-init
```

Поднять стенд в фоне:

```bash
docker compose up -d
```

Проверить статус контейнеров (дождаться `healthy`, 2–3 минуты):

```bash
docker compose ps
```

**UI Airflow:** http://localhost:8080
**Логин/пароль:** `airflow` / `airflow`

---

## Этап 2. Проверка базы данных

Проверить, что таблицы созданы:

```bash
docker compose exec analytics-db psql -U student -d analytics -c "\dt"
```

Проверить созданные Connection:

```bash
docker compose exec airflow-scheduler airflow connections list | grep iss
```

---

## Этап 3. Создание Connection

В UI Airflow: **Admin → Connections → +**

| Параметр    | Значение        |
|-------------|-----------------|
| Connection Id | `iss_postgres` |
| Type        | `Postgres`      |
| Host        | `analytics-db`  |
| Schema      | `analytics`     |
| Login       | `student`       |
| Password    | `student_pass`  |
| Port        | `5432`          |

---

## Этап 4. Запуск DAG

1. Включить DAG тумблером.
2. Нажать **Trigger** 6 раз.

Проверить список DAG'ов:

```bash
docker compose exec airflow-scheduler airflow dags list | grep iss
```

Проверить конкретный DAG:

```bash
docker compose exec airflow-scheduler airflow dags list | grep iss_position_pipeline
```

Проверить ошибки импорта DAG'ов:

```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
```

---

## Этап 5. Проверка данных в БД

Посмотреть все записи:

```bash
docker compose exec analytics-db psql -U student -d analytics -c "SELECT id, event_timestamp, latitude, longitude FROM iss_location ORDER BY id;"
```

Или полностью:

```bash
docker compose exec analytics-db psql -U student -d analytics -c "SELECT * FROM iss_location ORDER BY id;"
```

Посчитать количество записей:

```bash
docker compose exec analytics-db psql -U student -d analytics -t -c "SELECT COUNT(*) FROM iss_location;"
```

---

## Управление стендом

Остановить контейнеры (без удаления):

```bash
docker compose stop
```

Запустить обратно:

```bash
docker compose start
```

Полностью удалить стенд вместе с томами:

```bash
docker compose down -v
```

Логи воркера:

```bash
docker compose logs -f airflow-worker
```

Логи scheduler'а:

```bash
docker compose logs -f airflow-scheduler
```

Применить SQL-скрипт инициализации вручную:

```bash
docker compose exec -T analytics-db psql -U student -d analytics < sql/init.sql
```

---

## Полезные заметки

- Папки `screenshots/`, `plugins/`, `config/` должны существовать в репозитории.
  Если их нет — создать (в PowerShell):
  ```powershell
  mkdir screenshots, plugins, config -Force
  New-Item -ItemType File -Path screenshots/.gitkeep, plugins/.gitkeep, config/.gitkeep -Force
  ```
- В Unix-системах аналог:
  ```bash
  touch screenshots/.gitkeep plugins/.gitkeep config/.gitkeep
  ```


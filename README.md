# 🚀 Airflow ISS Pipeline | Домашнее задание

**Автор:** [Михаил Батаев](https://github.com/rodionmirov)  
**Курс:** OTUS Data Engineer  
**Тема:** Apache Airflow. Сложные пайплайны. Подготовка и установка на расписание DAG выгрузки данных из источников.

---

## 📋 Описание проекта
Данный проект представляет собой автоматический Data Pipeline, развернутый локально с помощью Docker Compose. 
Пайплайн каждые 30 минут обращается к публичному API [Open Notify (ISS Location)](http://api.open-notify.org/iss-now.json), парсит JSON-ответ (координаты Международной Космической Станции) и идемпотентно загружает данные в целевую базу данных PostgreSQL (`analytics`).

### Архитектура стенда
Стенд повторяет прод-архитектуру из вебинара (8 контейнеров):
*   **airflow-webserver** (UI на порту `8080`) — витрина, принимает команды.
*   **airflow-scheduler** — читает папку `dags/`, создает DAG Runs по расписанию.
*   **airflow-worker** — выполняет Python-код тасков.
*   **redis** — брокер сообщений (очередь задач).
*   **postgres** — метабаза Airflow (хранит статусы, XCom, Connections).
*   **analytics-db** (порт `5433`) — **целевая БД**, куда пишутся бизнес-данные.

---

## 🛠 Как развернуть стенд с нуля (Пошагово)

### Требования
1. Установленный [Docker Desktop](https://www.docker.com/products/docker-desktop/) (выделить минимум 4GB RAM в настройках Resources).
2. Установленный [Git](https://git-scm.com/).
3. Терминал **Git Bash** (или WSL).

### Шаг 1: Клонирование и подготовка
```bash
git clone https://github.com/rodionmirov/airflow-iss-homework.git
cd airflow-iss-homework
mkdir -p logs

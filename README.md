# Бот службы поддержки

Простой бот для службы поддержки с интеграцией DialogFlow, работающий в Telegram и VK. Не очень умный, но вполне способный отвечать на простые вопросы пользователя.

### Как установить

Клонируйте репозиторий, установите в директорию с проектом Python 3.12.3 или выше. Активируйте виртуальное окружение и установите зависимости:

```shell
git clone https://github.com/aigelia/customer-support-bot.git
cd customer-support-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Для запуска приложения вам понадобится сервисный аккаунт в консоли Google Cloud, аккаунт DialogFlow, а также аккаунты в Telegram и VK. Изучите документацию сервисов, чтобы получить нужные токены, описанные ниже.

С помощью Google Cloud получите сервисный ключи в формате JSON и поместите его в файл `credentials.json` в корне проекта. А также создайте файл .env в корне проекта и поместите туда следующие переменные: 

`TG_TOKEN` - токен бота Telegram;
`VK_TOKEN` - токен группы VK;
`GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу с сервисным ключом Google (по умолчанию укажите ./credentials.json);
`DIALOGFLOW_API_KEY` - API-ключ DialogFlow.

### Обучение DialogFlow

В программе также есть небольшой скрипт для обучения DialogFlow различным паттернам разговора. Для его работы нужен JSON-файл (пример также есть в директории проекта - `questions.json`). 

Соберите нужные нам вопросы и ответы в соответствующем формате в файле `questions.json` и запустите скрипт для добавления интентов:

```shell
python intent_creator.py
```

### Запуск на сервере

Для запуска на продакшене проделайте все вышеуказанные действия по установке и настройке, а после этого демонизируйте ботов. Для этого нужно создать и запустить юниты для `systemd` для каждого из ботов подобного содержания:

```
[Unit]
Description=Bot Description
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/venv/bin/python /path/to/project/vk_bot.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).
# Боты для Telegram и VK, использующие DialogFlow

Бэкэнд для ботов telegram и VK, использующих Google DialogFlow.
Dialogflow - это облачный сервис распознавания языка от Google.

## Как запустить локально на linux

* Скачайте код
* Перейдите в каталог проекта
* Установите зависимости `pip3 install -r requirements.txt`
* Создайте файл .env с переменными окружения (указаны ниже) и положите в каталог с проектом
* Экспортируйте переменные окружения `source .env`
* Создайте бота в telegram и начните с ним беседу
* Запустите бота `python3 telegram_bot.py` или `python3 vk_bot.py`
* Откройте в браузере 

## Настройки окружения. Пример:

```
export TELEGRAM_TOKEN='токен_полученный_при_регистрации_бота'
export CHAT_ID=ваш_chat_id
export GOOGLE_APPLICATION_CREDENTIALS="path_to_cred.json"
export PROJECT_ID="project_id"
export VK_TOKEN="Токен VK"
export LANGUAGE_CODE="ru"
```

## Цели проекта

Код написан в учебных целях.
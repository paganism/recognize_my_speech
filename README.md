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

## Управление собственными intents для DialogFlow через python

> Создаем файл.json с подобным содержимым:

```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
        ],
        "answer": "Напишите на почту мини-эссе о себе и прикрепите ваше портфолио."
    },
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?»"
    },
}
```
Далее используем скрипт intent.py

> Следующая команда создаст все intents из json-файла
```
python3 intent.py --action create --path  путь_к_файлу_с_intents.json
```
> Следующая команда покажет список всех intents
```
python3 intent.py --action list
```
> Следующая команда удалит intent по уникальному идентификатору
```
python3 intent.py --action delete --intent_id  уникальный_intent_uuid
```

## Цели проекта

Код написан в учебных целях.
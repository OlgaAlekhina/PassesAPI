Задача: разработать базу данных горных перевалов для Федерации Спортивного Туризма России и REST API для работы с мобильным приложением.

Задача реализована с помощью фрэймворка FastAPI и библиотеки pydantic. Для хранения информации о горных перевалах создана база данных PostgreSQL. Для подключения к базе данных использовалась библиотека psycorg2.

Интерактивная документация Swagger доступна по адресу http://127.0.0.1:8000/docs

API реализует следующие методы:

1. POST/addpass  для добавления нового перевала в базу данных

метод принимает JSON данные вида:
{
  "user": {
    "name": "Anna",
    "email": "anna@mail.ru",
    "phone": "555-55-55"
  },
  "passes": {
    "beauty_title": "pass",
    "title": "Anna",
    "other_titles": "string",
    "title_connect": "string",
    "data_added": "2022-07-04T11:49:01.127Z",
    "level_winter": "hard",
    "level_spring": "string",
    "level_summer": "easy",
    "level_autumn": "string",
    "latitude": 35,
    "longitude": 158,
    "height": 3000
  },
  "images": [
    {
      "title": "pic1",
      "url_path": "string",
      "data_added": "2022-07-04T11:49:01.127Z"
    },
{
      "title": "pic2",
      "url_path": "string",
      "data_added": "2022-07-04T11:49:01.127Z"
    },
{
      "title": "pic3",
      "url_path": "string",
      "data_added": "2022-07-04T11:49:01.127Z"
    }
  ]
}

возвращает {"status" : int, "message" : "str", "id" : int}, где status - HTTP код ответа сервера, message - результат операции, id - идентификатор созданного перевала

2. GET/passes/<pass_id>  для получения всей информации о перевале по его идентификатору
  
метод принимает id перевала
  
возвращает все данные о перевале в словаре вида:
{
"user": {
    "name": "Olga",
    "email": "olga@mail.ru",
    "phone": "555-55-55"
  },
  "passes": {
    "beauty_title": "best",
    "title": "OlgaPass",
    "other_titles": "small",
    "title_connect": "and",
    "data_added": "2022-07-01T20:13:25.416Z",
    "level_winter": "hard",
    "level_spring": "semi-hard",
    "level_summer": "easy",
    "level_autumn": "semi-hard",
    "latitude": 268,
    "longitude":57,
    "height": 2000
  },
  "images": [
    {
      "title": "pic1",
      "url_path": "mysite.ru/pic1",
      "data_added": "2022-07-01T20:13:25.416Z"
    },
{
      "title": "pic2",
      "url_path": "mysite.ru/pic2",
      "data_added": "2022-07-01T20:13:25.416Z"
    }
  ]
}
  
3. PATCH/update/<pass_id>  для частичного редактирования данных о перевале по его идентификатору

метод принимает id перевала и словарь с новыми данными вида:
{
    "title": "NewTitle",
    "level_winter": "not so hard",
    "level_autumn": "quite easy",
    "height": 3000
  }

возвращает {"state" : int, "message" : "str"}, где state = 1 при удачной операции, 0 при неудачной операции, message - причина ошибки

4. GET/passes/users/<user_email>  для получения информации обо всех перевалах, размещенных одним пользователем по его email

принимает email пользователя

возвращает список данных обо всех перевалах пользователя вида:
[
  {
    "beauty_title": "best",
    "title": "OlgaPass",
    "other_titles": "small",
    "title_connect": "and",
    "data_added": "2022-07-01T20:13:25.416Z",
    "level_winter": "hard",
    "level_spring": "semi-hard",
    "level_summer": "easy",
    "level_autumn": "semi-hard",
    "latitude": 268,
    "longitude":57,
    "height": 2000
  },
  {
    "beauty_title": "worst",
    "title": "Pass",
    "other_titles": "ever",
    "title_connect": "-",
    "data_added": "2022-07-01T20:21:54.416Z",
    "level_winter": "so-so",
    "level_spring": "easy",
    "level_summer": "easy",
    "level_autumn": "hard and dirty",
    "latitude": 578,
    "longitude":89,
    "height": 1500
  }
]

Задача: разработать базу данных горных перевалов для Федерации Спортивного Туризма России и REST API для работы с мобильным приложением.

Задача реализована с помощью фрэймворка FastAPI и библиотеки pydantic. Для хранения информации о горных перевалах создана база данных PostgreSQL. Для передачи данных между API и базой данных использовалась библиотека psycorg2.

API реализует следующие методы:

1. POST/addpass  для добавления нового перевала в базу данных

метод принимает JSON данные вида:
{
  "user": {
    "name": "string",
    "email": "string",
    "phone": "string"
  },
  "passes": {
    "beauty_title": "string",
    "title": "string",
    "other_titles": "string",
    "title_connect": "string",
    "data_added": "2022-07-01T19:53:29.691Z",
    "level_winter": "string",
    "level_spring": "string",
    "level_summer": "string",
    "level_autumn": "string",
    "latitude": 0,
    "longitude": 0,
    "height": 0
  },
  "images": [
    {
      "title": "string",
      "url_path": "string",
      "data_added": "2022-07-01T19:53:29.691Z"
    }
  ]
}

возвращает {"status" : int, "message" : "str", "id" : int}, где status - HTTP код ответа сервера, message - результат операции, id - id созданного перевала

2. GET/passes/<pass_id>  для получения всей информации о перевале по его id
  
метод принимает id перевала
  
возвращает все данные о перевале в словаре вида:
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
}'
  
3. PATCH/update/<pass_id>  для частичного редактирования данных о перевале по его id

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
[{
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
  }]

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime
from typing import List, Union
import psycopg2
from psycopg2 import Error

load_dotenv()

FSTR_DB_LOGIN = os.getenv('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.getenv('FSTR_DB_PASS')
FSTR_DB_HOST = os.getenv('FSTR_DB_HOST')
FSTR_DB_PORT = os.getenv('FSTR_DB_PORT')
FSTR_DB_NAME = os.getenv('FSTR_DB_NAME')


class User(BaseModel):
    name: str
    email: str
    phone: str = None

class Pass(BaseModel):
    beauty_title: str
    title: str
    other_titles: str = None
    title_connect: str = None
    data_added: datetime
    level_winter: str = None
    level_spring: str = None
    level_summer: str = None
    level_autumn: str = None
    latitude: float
    longitude: float
    height: int


class Image(BaseModel):
    title: str
    url_path: str
    data_added: datetime


class AddPass(BaseModel):
    user: User
    passes: Pass
    images: List[Image]

    def add_pass(self):
        try:
            # Подключиться к базе данных
            connection = psycopg2.connect(user=FSTR_DB_LOGIN,
                                          password=FSTR_DB_PASS,
                                          host=FSTR_DB_HOST,
                                          port=FSTR_DB_PORT,
                                          database=FSTR_DB_NAME)

            # Создать курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            # Проверка, если ли юзер в базе данных
            cursor.execute("SELECT id FROM users WHERE email=%s", (self.user.email,))
            user_id = cursor.fetchone()

            if user_id == None:
                # Вставить данные в таблицу Users
                insert_user_data = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s) RETURNING id;"
                cursor.execute(insert_user_data, (self.user.name, self.user.email, self.user.phone))
                # Получить id юзера
                user_id = cursor.fetchone()

            # Вставить данные в таблицу Passes
            insert_pass_data = '''INSERT INTO passes (beauty_title, title, other_titles, title_connect, data_added,
                                status, level_winter, level_spring, level_summer, level_autumn, latitude, longitude,
                                height, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'''
            cursor.execute(insert_pass_data, (self.passes.beauty_title, self.passes.title, self.passes.other_titles,
                                              self.passes.title_connect, self.passes.data_added, 'new',
                                              self.passes.level_winter, self.passes.level_spring, self.passes.level_summer,
                                              self.passes.level_autumn, self.passes.latitude, self.passes.longitude,
                                              self.passes.height, user_id))

            # Получить id перевала
            pass_id = cursor.fetchone()

            # Вставить данные в таблицу Images
            for image in self.images:
                insert_image_data = "INSERT INTO images (title, url_path, data_added, pass_id) VALUES (%s, %s, %s, %s);"
                cursor.execute(insert_image_data, (image.title, image.url_path, image.data_added, pass_id))

            connection.commit()
            print("Данные успешно добавлены в PostgreSQL")

            return pass_id[0]

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

class Response(BaseModel):
    status: int
    message: str
    id: Union[int, None]

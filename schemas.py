import os
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime
from typing import List, Union
import psycopg2


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
        connection = psycopg2.connect(user=FSTR_DB_LOGIN,
                                      password=FSTR_DB_PASS,
                                      host=FSTR_DB_HOST,
                                      port=FSTR_DB_PORT,
                                      database=FSTR_DB_NAME)
        with connection:
            with connection.cursor() as cursor:
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

                #Вставить данные в таблицу Images
                for image in self.images:
                    insert_image_data = "INSERT INTO images (title, url_path, data_added, pass_id) VALUES (%s, %s, %s, %s);"
                    cursor.execute(insert_image_data, (image.title, image.url_path, image.data_added, pass_id))

        connection.close()
        print("Данные успешно добавлены. Соединение с базой данных закрыто")

        return pass_id[0]

    # def update_pass(self, pass_id):
    #     connection = psycopg2.connect(user=FSTR_DB_LOGIN,
    #                                   password=FSTR_DB_PASS,
    #                                   host=FSTR_DB_HOST,
    #                                   port=FSTR_DB_PORT,
    #                                   database=FSTR_DB_NAME)
    #     with connection:
    #         with connection.cursor() as cursor:


class Response(BaseModel):
    status: int
    message: str
    id: Union[int, None]


def get_pass(pass_id):
    connection = psycopg2.connect(user=FSTR_DB_LOGIN,
                                  password=FSTR_DB_PASS,
                                  host=FSTR_DB_HOST,
                                  port=FSTR_DB_PORT,
                                  database=FSTR_DB_NAME)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT beauty_title, title, other_titles, title_connect, data_added, level_winter,
            level_spring, level_summer, level_autumn, latitude, longitude, height FROM passes WHERE id=%s''', (pass_id,))
            columns = [column[0] for column in cursor.description]
            pass_data = cursor.fetchone()
            pass_data = dict(zip(columns, pass_data))
            print(pass_data)
            cursor.execute('''SELECT users.name, users.email, users.phone FROM users, passes WHERE 
            passes.user_id=users.id AND passes.id=%s''', (pass_id,))
            columns = [column[0] for column in cursor.description]
            user_data = cursor.fetchone()
            user_data = dict(zip(columns, user_data))
            print(user_data)
            cursor.execute('''SELECT images.title, images.url_path, images.data_added FROM images, passes WHERE 
            images.pass_id=passes.id AND passes.id=%s''', (pass_id,))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            image_data = []
            for row in rows:
                image_dict = dict(zip(columns, row))
                image_data.append(image_dict)

            return {"user" : user_data, "passes": pass_data, "images": image_data}

    connection.close()
    



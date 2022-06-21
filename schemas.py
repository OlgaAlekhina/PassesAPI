from pydantic import BaseModel
from datetime import datetime
from typing import List
import psycopg2
from psycopg2 import Error


class User(BaseModel):
    """Validate request data."""
    name: str
    email: str
    phone: str = None

class Pass(BaseModel):
    """Validate request data."""
    beauty_title: str
    title: str
    other_titles: str = None
    title_connect: str = None
    data_added: datetime
    status: str = 'new'
    level_winter: str = None
    level_spring: str = None
    level_summer: str = None
    level_autumn: str = None
    latitude: float
    longitude: float
    height: int
    user_id: int


class Image(BaseModel):
    title: str
    image_file: bytes
    data_added: datetime
    pass_id: int


class AddPass(BaseModel):
    user: User
    passes: Pass
    images: List[Image]

    def add_pass(self):
        try:
            # Подключиться к существующей базе данных
            connection = psycopg2.connect(user="postgres",
                                          # пароль, который указали при установке PostgreSQL
                                          password="cyrkrobo",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres")

            # Создайте курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            # SQL-запрос для вставки данных
            insert_user_data = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s);"

            # Выполнение команды: это вставит данные в таблицу
            cursor.execute(insert_user_data, (self.user.name, self.user.email, self.user.phone))
            connection.commit()
            print(self.user.name)
            print(self.user.email)
            print(self.user.phone)
            print("Данные успешно добавлены в PostgreSQL")

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

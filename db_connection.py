import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()

FSTR_DB_LOGIN = os.getenv('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.getenv('FSTR_DB_PASS')
FSTR_DB_HOST = os.getenv('FSTR_DB_HOST')
FSTR_DB_PORT = os.getenv('FSTR_DB_PORT')
FSTR_DB_NAME = os.getenv('FSTR_DB_NAME')


def connect_db():
    db_connection = psycopg2.connect(user=FSTR_DB_LOGIN,
                                      password=FSTR_DB_PASS,
                                      host=FSTR_DB_HOST,
                                      port=FSTR_DB_PORT,
                                      database=FSTR_DB_NAME)
    return db_connection


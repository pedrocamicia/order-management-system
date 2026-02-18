import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_CONFIG = {
    "host" : os.getenv("DB_HOST"),
    "dbname" : os.getenv("DB_NAME"),
    "user" : os.getenv("DB_USER"),
    "password" : os.getenv("DB_PASSWORD"),
    "port" : int(os.getenv("DB_PORT"))
}


def conectar():
    return psycopg2.connect(**DB_CONFIG)
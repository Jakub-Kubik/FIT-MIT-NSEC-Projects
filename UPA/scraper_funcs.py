import os

from datetime import datetime

import requests
import rfc3339

from influxdb import InfluxDBClient


def connect_to_db():
    host = os.getenv("INFLUX_HOST")
    port = os.getenv("INFLUX_PORT")
    login = os.getenv("INFLUX_LOGIN")
    password = os.getenv("INFLUX_PASSWORD")

    default_db = "_internal"  # default system db

    return InfluxDBClient(host, port, login, password, default_db)


def create_and_switch_to_db(client, db_name):
    print(f"Create database: {db_name}")
    client.create_database(db_name)

    print(f"Switch to database: {db_name}")
    client.switch_database(db_name)


def convert_date_to_rfc3339_format(date):
    try:
        int(date)
        date = datetime.fromtimestamp(int(date))
    except Exception:
        if isinstance(date, str):
            date = datetime.fromisoformat(date)
    return rfc3339.rfc3339(date)


def download_csv_data(url):
    return requests.get(url).content.decode("utf-8-sig")
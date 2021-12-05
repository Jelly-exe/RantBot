import sqlite3
import yaml

with open("bot.yml", "r") as ymlfile:
    bot = yaml.load(ymlfile, Loader=yaml.FullLoader)

connection = sqlite3.connect("Database.db")
cursor = connection.cursor()


def fetch(query):
    cursor.execute(query)
    return cursor.fetchall()


def insert(query, values):
    cursor.execute(query, values)
    connection.commit()


def update(query):
    cursor.execute(query)
    connection.commit()

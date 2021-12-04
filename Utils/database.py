import mysql.connector.pooling
import yaml

with open("bot.yml", "r") as ymlfile:
    bot = yaml.load(ymlfile, Loader=yaml.FullLoader)

database = mysql.connector.pooling.MySQLConnectionPool(
    host=bot["database"]["host"],
    user=bot["database"]["username"],
    password=bot["database"]["password"],
    database=bot["database"]["name"],
    pool_name='Database',
    pool_size=25
)


def fetch(query):
    """Get a connection and a cursor from the pool"""
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    """Return the connection to the pool"""
    connection.close()
    return result


def insert(query, values):
    """Get a connection and a cursor from the pool"""
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute(query, values)
    connection.commit()

    connection.close()


def update(query):
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    connection.commit()

    connection.close()


def updateCache(querys):
    connection = database.get_connection()
    cursor = connection.cursor()

    for query in querys:
        cursor.execute(query)

    connection.commit()
    connection.close()

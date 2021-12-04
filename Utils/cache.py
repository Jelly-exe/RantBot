from Utils.database import fetch


class cache:
    def __init__(self, config):
        self.cache = {}
        self.dbChanges = {}
        self.config = config

        users = fetch(f'SELECT * FROM Users')

        self.cache["users"] = {int(i[0]): {'puuid': i[1], 'gameName': i[2], 'tagLine': i[3]} for i in users}

        self.dbChanges["users"] = {}

    def getUser(self, userId):
        return self.cache["users"][userId]

    def updateUsers(self, userId, key, value):
        self.cache["users"][userId][key] = value

        if userId not in self.dbChanges["users"]:
            self.dbChanges["users"][userId] = {key: value}
        else:
            self.dbChanges["users"][userId][key] = value

    def generateSQL(self):
        sql = []
        sql += self._usersSQL()

        return sql

    def _usersSQL(self):
        sql = []

        for user in self.dbChanges["users"]:
            setString = ''

            for key in self.dbChanges["users"][user]:
                setString += f'{key} = "{self.dbChanges["users"][user][key]}", '

            sql.append(f'UPDATE Users SET {setString[:-2]} WHERE userId = "{user}"')

        self.dbChanges["users"] = {}

        return sql

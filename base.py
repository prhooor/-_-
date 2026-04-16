import sqlite3

class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # Добавление пользователя в БД
    def add_user(self, id):
        query = "INSERT INTO users (id) VALUES(?)"
        with self.connection:
            return self.cursor.execute(query, (id,))

    def add_project(self, user_id, project_name):
        query = "INSERT INTO project (user_id, project_name) VALUES(?,?)"
        with self.connection:
            return self.cursor.execute(query, (user_id,project_name,))

    def add_object(self, user_id, project_id, project_name):
        query = "INSERT INTO objects (user_id, project_id, project_name) VALUES(?,?,?)"
        with self.connection:
            return self.cursor.execute(query, (user_id,project_id,project_name,))


    # Проверка, есть ли пользователь в БД
    def user_exist(self, id):
        query = "SELECT * FROM users WHERE id = ?"
        with self.connection:
            result = self.cursor.execute(query, (id,)).fetchall()
            return bool(len(result))

    # Получить значение поля
    def get_field(self, table, id, field):
        query = f"SELECT {field} FROM {table} WHERE id = ?"
        with self.connection:
            result = self.cursor.execute(query, (id,)).fetchone()
            if result:
                return result[0]

    def get_all(self, table):
        query = f"SELECT * FROM {table}"
        with self.connection:
            result = self.cursor.execute(query).fetchall()
            if result:
                return result

    def get_objects_by_project(self, id, project_id):
        query = f"SELECT id FROM objects WHERE project_id = {project_id}"
        with self.connection:
            result = self.cursor.execute(query).fetchall()
            if result:
                return result

    def get_object_by_idk(self, project_id, project_name, user_id):
        query = f"SELECT id FROM objects WHERE project_id = {project_id} AND project_name = {project_name} AND user_id = {user_id}"
        with self.connection:
            item = self.cursor.execute(query).fetchone()
            if item:
                return item [0]
            else:
                return -1


    # Обновить значение поля
    def update_field(self, table, id, field, value):
        query = f"UPDATE {table} SET {field} = ? WHERE id = ?"
        with self.connection:
            self.cursor.execute(query, (value, id))

    def close(self):
        self.connection.close()

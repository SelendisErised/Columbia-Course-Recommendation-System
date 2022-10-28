import pymysql

class DatabaseConnection:
    def __init__(self, host, database_user_id, database_user_password, default_scheme):
        self.host = host
        self.database_user_id = database_user_id
        self.database_user_password = database_user_password
        self.default_scheme = default_scheme

    def connection(self):
        conn = pymysql.connect(
        host = self.host,
        user = self.database_user_id, 
        password = self.database_user_password,
        db = self.default_scheme,
        )
        cur = conn.cursor()
        return cur

class SearchFunction:
    def __init__(self, default_scheme, table_name):
        self.database_name = default_scheme
        self.table_name = table_name

    def ambiguous_search(self, string):
        mysql = "select * from {}.{} where Course like '%{}%' or CourseTitle like '%{}%' or CourseSubtitle like '%{}%'".format(self.database_name, self.table_name, string, string, string)
        return mysql




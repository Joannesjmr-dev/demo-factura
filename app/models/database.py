import mysql.connector

class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='admin', database='facturas_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            self.conn = None
            return False

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query, params=None):
        if self.conn is None:
            if not self.connect():
                return False
        if self.conn is None:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error ejecutando query: {err}")
            return False

    def fetch_all(self, query, params=None):
        if self.conn is None:
            if not self.connect():
                return []
        if self.conn is None:
            return []
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            print(f"Error en fetch_all: {err}")
            return [] 
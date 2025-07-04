"""Módulo: DatabaseManager"""
import mysql.connector
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestor de base de datos MySQL"""
    
    def __init__(self, host='localhost', database='facturas_db', user='root', password='admin'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                logger.info("✅ Conexión exitosa a MySQL")
                print("✅ Conexión exitosa a MySQL")  # <--- Agregado
                return True
        except Error as e:
            logger.error(f"❌ Error conectando a MySQL: {e}")
            print(f"❌ Error conectando a MySQL: {e}")  # ⬅️ TEMPORAL
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión MySQL cerrada")
    
    def execute_query(self, query, params=None):
        """Ejecutar consulta SQL"""
        if not self.connection or not self.connection.is_connected():
            logger.error("No hay conexión activa a la base de datos.")
            return None
    
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        """Obtener todos los resultados de una consulta"""
        if not self.connection or not self.connection.is_connected():
            logger.error("No hay conexión activa a la base de datos.")
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            logger.error(f"Error en consulta: {e}")
            return []

"""Módulo: DatabaseManager mejorado con singleton y conexión automática"""
import mysql.connector
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestor de base de datos MySQL (singleton con conexión automática)"""
    
    _instance = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, host='localhost', database='facturas_db', user='root', password='admin'):
        if not hasattr(self, 'initialized'):  # Evita re-ejecutar init
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.connection = None
            self.initialized = True
            self.connect()  # 👈 Se conecta automáticamente

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
                print("✅ Conexión exitosa a MySQL")
                return True
        except Error as e:
            logger.error(f"❌ Error conectando a MySQL: {e}")
            print(f"❌ Error conectando a MySQL: {e}")
            self.connection = None
        return False

    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("🔌 Conexión MySQL cerrada")

    def execute_query(self, query, params=None):
        """Ejecutar consulta SQL"""
        if not self.connection or not self.connection.is_connected():
            logger.warning("⛔ No hay conexión activa. Reconectando...")
            if not self.connect():
                return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error(f"❌ Error ejecutando consulta: {e}")
            return None

    def fetch_all(self, query, params=None):
        """Obtener todos los resultados de una consulta"""
        if not self.connection or not self.connection.is_connected():
            logger.warning("⛔ No hay conexión activa. Reconectando...")
            if not self.connect():
                return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            logger.error(f"❌ Error en consulta: {e}")
            return []

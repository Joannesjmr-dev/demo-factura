"""Módulo: ConfiguracionApp"""
import os
import json
import logging

logger = logging.getLogger(__name__)

class ConfiguracionApp:
    """Configuración de la aplicación"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.config = self.cargar_config()
    
    def cargar_config(self):
        """Cargar configuración desde archivo"""
        config_default = {
            "database": {
                "host": "localhost",
                "database": "facturas_db",
                "user": "root",
                "password": "admin"
            },
            "empresa": {
                "nit": "",
                "razon_social": "",
                "direccion": "",
                "telefono": "",
                "email": ""
            },
            "dian": {
                "ambiente": "habilitacion",  # habilitacion o produccion
                "pin_software": "",
                "id_software": ""
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Combinar con defaults
                    return {**config_default, **config}
            return config_default
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            return config_default
    
    def guardar_config(self):
        """Guardar configuración a archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
            return False
    
    def get(self, seccion, clave, default=None):
        """Obtener valor de configuración"""
        return self.config.get(seccion, {}).get(clave, default)
    
    def set(self, seccion, clave, valor):
        """Establecer valor de configuración"""
        if seccion not in self.config:
            self.config[seccion] = {}
        self.config[seccion][clave] = valor

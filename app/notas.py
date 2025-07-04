"""Módulo: NotaCreditoDebito"""

import logging
from datetime import datetime
from decimal import Decimal
import hashlib


class NotaCreditoDebito:
    """Clase base para Notas Crédito y Débito"""
    
    def __init__(self, tipo_nota):
        self.tipo_nota = tipo_nota  # 'credito' o 'debito'
        self.datos = {
            'numero': '',
            'fecha_emision': datetime.now().strftime('%Y-%m-%d'),
            'hora_emision': datetime.now().strftime('%H:%M:%S'),
            'factura_referencia': '',
            'codigo_concepto': '',
            'descripcion_concepto': '',
            'valor_base': Decimal('0.00'),
            'porcentaje_iva': Decimal('19.00'),
            'valor_iva': Decimal('0.00'),
            'valor_total': Decimal('0.00'),
            'cufe': '',
            'qr_code': ''
        }
        self.emisor = {}
        self.adquiriente = {}
        
    def calcular_valores(self):
        """Calcular valores de IVA y total"""
        base = self.datos['valor_base']
        porcentaje = self.datos['porcentaje_iva']
        
        self.datos['valor_iva'] = (base * porcentaje / 100).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        self.datos['valor_total'] = base + self.datos['valor_iva']
    
    def generar_cufe(self):
        """Generar CUFE según especificaciones DIAN"""
        # Datos para el CUFE
        cufe_data = (
            f"{self.datos['numero']}"
            f"{self.datos['fecha_emision']}"
            f"{self.datos['hora_emision']}"
            f"{self.datos['valor_total']:.2f}"
            f"{self.emisor.get('nit', '')}"
            f"{self.adquiriente.get('nit', '')}"
        )
        
        # Hash SHA-384
        hash_obj = hashlib.sha384(cufe_data.encode('utf-8'))
        self.datos['cufe'] = hash_obj.hexdigest()
        
    def validar_datos(self):
        """Validar datos obligatorios"""
        campos_obligatorios = [
            'numero', 'fecha_emision', 'factura_referencia',
            'codigo_concepto', 'valor_base'
        ]
        
        for campo in campos_obligatorios:
            if not self.datos.get(campo):
                return False, f"Campo obligatorio faltante: {campo}"
        
        return True, "Validación exitosa"

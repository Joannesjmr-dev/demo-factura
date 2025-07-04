"""Módulo: ValidadorDIAN"""

import logging
from datetime import datetime

class ValidadorDIAN:
    """Validador de documentos según normativa DIAN"""
    
    @staticmethod
    def validar_nit(nit):
        """Validar NIT con dígito verificador"""
        if not nit or len(nit) < 3:
            return False
        
        # Extraer dígitos
        nit_digits = nit.replace('-', '').replace('.', '')
        if not nit_digits.isdigit():
            return False
        
        # Calcular dígito verificador
        weights = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
        nit_number = nit_digits[:-1]
        check_digit = int(nit_digits[-1])
        
        total = 0
        for i, digit in enumerate(reversed(nit_number)):
            if i < len(weights):
                total += int(digit) * weights[i]
        
        remainder = total % 11
        calculated_check = 11 - remainder if remainder > 1 else remainder
        
        return calculated_check == check_digit
    
    @staticmethod
    def validar_fecha(fecha_str):
        """Validar formato de fecha"""
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_concepto_nota_credito(codigo):
        """Validar conceptos de nota crédito según DIAN"""
        conceptos_validos = ['1', '2', '3', '4', '5', '6']
        return codigo.split(' - ')[0] in conceptos_validos if ' - ' in codigo else codigo in conceptos_validos
    
    @staticmethod
    def validar_concepto_nota_debito(codigo):
        """Validar conceptos de nota débito según DIAN"""
        conceptos_validos = ['1', '2', '3', '4']
        return codigo.split(' - ')[0] in conceptos_validos if ' - ' in codigo else codigo in conceptos_validos

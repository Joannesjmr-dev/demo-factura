"""Utilidades para validaciones DIAN y generador XML"""

import logging
from datetime import datetime
from decimal import Decimal
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

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

class GeneradorXML:
    """Generador de XML según especificaciones DIAN"""

    def __init__(self, nota):
        self.nota = nota

    def generar_xml(self):
        """Generar XML de la nota"""
        # Namespace DIAN
        ns = {
            'fe': 'urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2' if self.nota.tipo == 'credito' else 'urn:oasis:names:specification:ubl:schema:xsd:DebitNote-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        }

        # Elemento raíz
        if self.nota.tipo == 'credito':
            root = ET.Element('CreditNote', attrib={
                'xmlns': ns['fe'],
                'xmlns:cbc': ns['cbc'],
                'xmlns:cac': ns['cac']
            })
        else:
            root = ET.Element('DebitNote', attrib={
                'xmlns': ns['fe'],
                'xmlns:cbc': ns['cbc'],
                'xmlns:cac': ns['cac']
            })

        # Elementos básicos
        ET.SubElement(root, f"{{{ns['cbc']}}}ID").text = self.nota.numero
        ET.SubElement(root, f"{{{ns['cbc']}}}IssueDate").text = self.nota.fecha_emision.strftime('%Y-%m-%d')
        ET.SubElement(root, f"{{{ns['cbc']}}}IssueTime").text = self.nota.hora_emision.strftime('%H:%M:%S')

        # Referencia a factura
        billing_ref = ET.SubElement(root, f"{{{ns['cac']}}}BillingReference")
        invoice_ref = ET.SubElement(billing_ref, f"{{{ns['cac']}}}InvoiceDocumentReference")
        ET.SubElement(invoice_ref, f"{{{ns['cbc']}}}ID").text = self.nota.factura_referencia

        # Líneas de la nota
        line = ET.SubElement(root, f"{{{ns['cac']}}}{'CreditNoteLine' if self.nota.tipo == 'credito' else 'DebitNoteLine'}")
        ET.SubElement(line, f"{{{ns['cbc']}}}ID").text = "1"

        # Cantidad y valor
        quantity = ET.SubElement(line, f"{{{ns['cbc']}}}CreditedQuantity")
        quantity.text = "1"
        quantity.set('unitCode', 'NIU')

        # Valor línea
        line_amount = ET.SubElement(line, f"{{{ns['cbc']}}}LineExtensionAmount")
        line_amount.text = str(self.nota.valor_base)
        line_amount.set('currencyID', 'COP')

        return ET.tostring(root, encoding='unicode')
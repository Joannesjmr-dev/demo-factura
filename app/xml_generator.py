"""Módulo: GeneradorXML"""

import logging

class GeneradorXML:
    """Generador de XML según especificaciones DIAN"""
    
    def __init__(self, nota):
        self.nota = nota
        
    def generar_xml(self):
        """Generar XML de la nota"""
        # Namespace DIAN
        ns = {
            'fe': 'urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        }
        
        # Elemento raíz
        if self.nota.tipo_nota == 'credito':
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
        ET.SubElement(root, f"{{{ns['cbc']}}}ID").text = self.nota.datos['numero']
        ET.SubElement(root, f"{{{ns['cbc']}}}IssueDate").text = self.nota.datos['fecha_emision']
        ET.SubElement(root, f"{{{ns['cbc']}}}IssueTime").text = self.nota.datos['hora_emision']
        
        # Referencia a factura
        billing_ref = ET.SubElement(root, f"{{{ns['cac']}}}BillingReference")
        invoice_ref = ET.SubElement(billing_ref, f"{{{ns['cac']}}}InvoiceDocumentReference")
        ET.SubElement(invoice_ref, f"{{{ns['cbc']}}}ID").text = self.nota.datos['factura_referencia']
        
        # Líneas de la nota
        line = ET.SubElement(root, f"{{{ns['cac']}}}{'CreditNoteLine' if self.nota.tipo_nota == 'credito' else 'DebitNoteLine'}")
        ET.SubElement(line, f"{{{ns['cbc']}}}ID").text = "1"
        
        # Cantidad y valor
        quantity = ET.SubElement(line, f"{{{ns['cbc']}}}CreditedQuantity")
        quantity.text = "1"
        quantity.set('unitCode', 'NIU')
        
        # Valor línea
        line_amount = ET.SubElement(line, f"{{{ns['cbc']}}}LineExtensionAmount")
        line_amount.text = str(self.nota.datos['valor_base'])
        line_amount.set('currencyID', 'COP')
        
        return ET.tostring(root, encoding='unicode')

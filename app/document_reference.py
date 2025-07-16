import datetime

class DocumentReference:
    """
    Representa las referencias de un documento, como una factura.
    """
    def __init__(self, numero_factura: str, fecha_emision: datetime.date,
                 nit_emisor: str, razon_social: str, total_bruto_factura: float):
        if not isinstance(numero_factura, str) or not numero_factura:
            raise ValueError("El número de factura no puede estar vacío y debe ser una cadena de texto.")
        if not isinstance(fecha_emision, datetime.date):
            raise ValueError("La fecha de emisión debe ser un objeto datetime.date.")
        if not isinstance(nit_emisor, str) or not nit_emisor:
            raise ValueError("El NIT del emisor no puede estar vacío y debe ser una cadena de texto.")
        if not isinstance(razon_social, str) or not razon_social:
            raise ValueError("La razón social no puede estar vacía y debe ser una cadena de texto.")
        if not isinstance(total_bruto_factura, (int, float)) or total_bruto_factura < 0:
            raise ValueError("El total bruto de la factura debe ser un número positivo.")

        self.numero_factura = numero_factura
        self.fecha_emision = fecha_emision
        self.nit_emisor = nit_emisor
        self.razon_social = razon_social
        self.total_bruto_factura = total_bruto_factura

    def __str__(self):
        return (f"--- Referencias del Documento ---\n"
                f"Número de Factura: {self.numero_factura}\n"
                f"Fecha de Emisión: {self.fecha_emision.strftime('%Y-%m-%d')}\n"
                f"NIT del Emisor: {self.nit_emisor}\n"
                f"Razón Social: {self.razon_social}\n"
                f"Total Bruto Factura: {self.total_bruto_factura:,.2f}")

    def to_dict(self):
        """
        Convierte la referencia del documento a un diccionario.
        Útil para serialización (ej. a JSON).
        """
        return {
            "numero_factura": self.numero_factura,
            "fecha_emision": self.fecha_emision.strftime('%Y-%m-%d'),
            "nit_emisor": self.nit_emisor,
            "razon_social": self.razon_social,
            "total_bruto_factura": self.total_bruto_factura
        }

class NotaCreditoDebito:
    def __init__(self, tipo_nota):
        self.tipo_nota = tipo_nota
        self.datos = {}

    def validar_datos(self):
        # Implementar validación de datos de la nota
        return True, "" 
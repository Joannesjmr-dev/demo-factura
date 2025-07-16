from app.models.nota import NotaCreditoDebito
from app.models.database import DatabaseManager

class NotasController:
    def __init__(self, view):
        self.view = view
        self.db = DatabaseManager()
        self.db.connect()

    def generar_nota(self, datos_formulario):
        nota = NotaCreditoDebito(datos_formulario['tipo_nota'])
        nota.datos = datos_formulario
        valido, mensaje = nota.validar_datos()
        if not valido:
            self.view.mostrar_mensaje(mensaje)
            return
        # Guardar en BD
        query = """
        INSERT INTO notas_credito_debito
        (numero, tipo, fecha_emision, hora_emision, factura_referencia,
         codigo_concepto, descripcion_concepto, valor_base, porcentaje_iva,
         valor_iva, retencion_renta, porcentaje_retencion, valor_total, cufe, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            datos_formulario['numero'],
            datos_formulario['tipo_nota'],
            datos_formulario['fecha_emision'],
            datos_formulario.get('hora_emision', ''),
            datos_formulario['factura_referencia'],
            datos_formulario['codigo_concepto'],
            datos_formulario['descripcion_concepto'],
            float(datos_formulario['valor_base']),
            float(datos_formulario['porcentaje_iva']),
            float(datos_formulario['valor_iva']),
            float(datos_formulario['retencion_renta']),
            float(datos_formulario['porcentaje_retencion']),
            float(datos_formulario['valor_total']),
            datos_formulario.get('cufe', ''),
            'generado'
        )
        if self.db.execute_query(query, params):
            self.view.mostrar_mensaje('Nota generada con éxito')
        else:
            self.view.mostrar_mensaje('Error al guardar la nota')

    def consultar_notas(self, filtros):
        query = """
        SELECT numero, tipo, fecha_emision, factura_referencia,
               valor_total, estado
        FROM notas_credito_debito
        WHERE fecha_emision BETWEEN %s AND %s
        """
        params = [filtros['fecha_desde'], filtros['fecha_hasta']]
        if filtros['tipo'] != "Todos":
            tipo_filtro = "credito" if filtros['tipo'] == "Nota Crédito" else "debito"
            query += " AND tipo = %s"
            params.append(tipo_filtro)
        query += " ORDER BY fecha_emision DESC, numero DESC"
        resultados = self.db.fetch_all(query, params)
        if resultados:
            self.view.mostrar_resultados(resultados)
        else:
            self.view.mostrar_mensaje("No se encontraron registros") 
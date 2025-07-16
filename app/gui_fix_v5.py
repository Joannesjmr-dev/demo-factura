"""Módulo: InterfazNotas"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as ttkb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
# print(dir(ttkb))

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import logging

from app.database_v2 import DatabaseManager
from app.notas import NotaCreditoDebito
from app.xml_generator import GeneradorXML

logger = logging.getLogger(__name__)

class InterfazNotas:
    """Interfaz gráfica principal"""

    def __init__(self):
        self.root = ttkb.Window(themename="litera")
        self.root.title("Módulo Notas Crédito y Débito - DIAN")
        self.root.geometry("1200x800")

        self.db = DatabaseManager()
        self.nota_actual = None

        self.setup_ui()
        self.connect_database()

    def setup_ui(self):
        """Configurar interfaz de usuario"""
        # Frame principal
        main_frame = ttkb.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # Título
        title_label = ttkb.Label(
            main_frame,
            text="Módulo Notas Crédito y Débito - DIAN",
            font=("Arial", 16, "bold"),
            bootstyle=PRIMARY
        )
        title_label.pack(pady=(0, 20))

        # Notebook para pestañas
        self.notebook = ttkb.Notebook(main_frame)
        self.notebook.pack(fill=BOTH, expand=True)

        # Pestaña Nota Crédito
        self.tab_credito = ttkb.Frame(self.notebook)
        self.notebook.add(self.tab_credito, text="Nota Crédito")
        self.setup_nota_tab(self.tab_credito, 'credito')

        # Pestaña Nota Débito
        self.tab_debito = ttkb.Frame(self.notebook)
        self.notebook.add(self.tab_debito, text="Nota Débito")
        self.setup_nota_tab(self.tab_debito, 'debito')

        # Pestaña Consultas
        self.tab_consultas = ttkb.Frame(self.notebook)
        self.notebook.add(self.tab_consultas, text="Consultas")
        self.setup_consultas_tab()

    def crear_boton(self, parent, text, command, bootstyle=PRIMARY, side=LEFT, padx=(0, 10)):
        """Crea un botón con los parámetros dados y lo agrega al parent."""
        btn = ttkb.Button(parent, text=text, bootstyle=bootstyle, command=command)
        btn.pack(side=side, padx=padx)
        return btn

    def crear_entry(self, parent, label, var, row, column, width=15):
        """Crea un label y un entry en el grid especificado y retorna el entry."""
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.W, pady=(5, 0))
        entry = ttkb.Entry(parent, textvariable=var, width=width)
        entry.grid(row=row, column=column+1, padx=(5, 20), pady=(5, 0))
        return entry

    def crear_entry_readonly(self, parent, label, var, row, column, width=15):
        """Crea un label y un entry de solo lectura en el grid especificado y retorna el entry."""
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.W, pady=(5, 0))
        entry = ttkb.Entry(parent, textvariable=var, width=width, state=READONLY)
        entry.grid(row=row, column=column+1, padx=(5, 20), pady=(5, 0))
        return entry

    def crear_combobox(self, parent, label, var, values, row, column, width=40):
        """Crea un label y un combobox en el grid especificado y retorna el combobox."""
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.W)
        combo = ttkb.Combobox(parent, textvariable=var, values=values, width=width)
        combo.grid(row=row, column=column+1, padx=(5, 0))
        return combo

    def crear_text_multilinea(self, parent, label, row, column, width=50, height=3):
        """Crea un label y un campo de texto multilínea en el grid especificado y retorna el widget Text."""
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.NW, pady=(5, 0))
        text_widget = tk.Text(parent, height=height, width=width)
        text_widget.grid(row=row, column=column+1, padx=(5, 0), pady=(5, 0))
        return text_widget

    def crear_labelframe(self, parent, text, padding=10):
        """Crea un LabelFrame con el texto y padding dados y lo retorna."""
        frame = ttkb.LabelFrame(parent, text=text, padding=padding)
        frame.pack(fill=tk.X, pady=(0, 10))
        return frame

    def setup_nota_tab(self, parent, tipo_nota):
        """Configurar pestaña de nota"""
        # Frame de datos básicos
        datos_frame = self.crear_labelframe(parent, "Datos Básicos")

        # Número de nota
        ttkb.Label(datos_frame, text="Número:").grid(row=0, column=0, sticky=W, padx=(0, 20))
        numero_var = tk.StringVar()
        setattr(self, f'numero_{tipo_nota}_var', numero_var)
        ttkb.Entry(datos_frame, textvariable=numero_var, width=20).grid(row=1, column=0, padx=(5, 20))

        # Fecha (usar datetime ya importado globalmente)
        ttkb.Label(datos_frame, text="Fecha:").grid(row=0, column=1, sticky=W, padx=(0, 20))
        fecha_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        setattr(self, f'fecha_{tipo_nota}_var', fecha_var)
        ttkb.Entry(datos_frame, textvariable=fecha_var, width=15).grid(row=1, column=1, padx=(5, 20))

        # Referencias del documento
        Referencias_documento_frame = self.crear_labelframe(parent, "Referencias del documento")

        # Factura referencia
        ttkb.Label(Referencias_documento_frame, text="Factura Referencia:").grid(row=0, column=0, sticky=W, padx=(0, 20))
        factura_ref_var = tk.StringVar()
        setattr(self, f'factura_ref_{tipo_nota}_var', factura_ref_var)
        ttkb.Entry(Referencias_documento_frame, textvariable=factura_ref_var, width=20).grid(row=1, column=0, padx=(5, 20))

        # Fecha de Emisión
        ttkb.Label(Referencias_documento_frame, text="Fecha de Emisión:").grid(row=0, column=1, sticky=W, padx=(0, 20))
        fecha_emision_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        setattr(self, f'fecha_emision_{tipo_nota}_var', fecha_emision_var)
        ttkb.Entry(Referencias_documento_frame, textvariable=fecha_emision_var, width=15).grid(row=1, column=1, padx=(5, 20))

        # Nit del Emisor
        ttkb.Label(Referencias_documento_frame, text="Nit del Emisor:").grid(row=0, column=2, sticky=W, padx=(0, 20))
        nit_emisor_var = tk.StringVar()
        setattr(self, f'nit_emisor_{tipo_nota}_var', nit_emisor_var)
        ttkb.Entry(Referencias_documento_frame, textvariable=nit_emisor_var, width=20).grid(row=1, column=2, padx=(5, 20))

        # Razón Social del Emisor
        ttkb.Label(Referencias_documento_frame, text="Razón Social del Emisor:").grid(
            row=0, column=3, sticky=W, padx=(0, 20)
        )
        raz_soc_emisor_var = tk.StringVar()
        setattr(self, f'raz_soc_emisor_{tipo_nota}_var', raz_soc_emisor_var)
        ttkb.Entry(Referencias_documento_frame, textvariable=raz_soc_emisor_var, width=40).grid(row=1, column=3, padx=(5, 20))

        #Total Bruto Factura
        ttkb.Label(Referencias_documento_frame, text="Total Bruto Factura:").grid(
            row=0, column=4, sticky=W, padx=(0, 20)
        )
        total_bruto_var = tk.StringVar(value="0.00")
        setattr(self, f'total_bruto_{tipo_nota}_var', total_bruto_var)
        ttkb.Entry(Referencias_documento_frame, textvariable=total_bruto_var, width=15).grid(row=1, column=4, padx=(5, 20))

        # Concepto De Corrección
        concepto_frame = self.crear_labelframe(parent, "Concepto De Corrección")

        codigo_concepto_var = tk.StringVar()
        setattr(self, f'codigo_concepto_{tipo_nota}_var', codigo_concepto_var)
        conceptos_nota_credito = [
            "1 - Devolución parcial de los bienes y/o no aceptación parcial del servicio",
            "2 - Anulación de factura electrónica",
            "3 - Rebaja o descuento parcial o total",
            "4 - Ajuste de precio",
            "5 - Descuento comercial por pronto pago",
            "6 - Descuento comercial por volumen de ventas",
            "7 - Otros"
        ]
        self.crear_combobox(concepto_frame, "Código Concepto:", codigo_concepto_var, conceptos_nota_credito, 0, 0, width=40)

        descripcion_var = tk.StringVar()
        setattr(self, f'descripcion_{tipo_nota}_var', descripcion_var)
        descripcion_text = self.crear_text_multilinea(concepto_frame, "Descripción:", 1, 0, width=50, height=3)
        setattr(self, f'descripcion_{tipo_nota}_text', descripcion_text)

        # Valores
        valores_frame = self.crear_labelframe(parent, "Valores")

        valor_base_var = tk.StringVar(value="0.00")
        setattr(self, f'valor_base_{tipo_nota}_var', valor_base_var)
        entry_base = self.crear_entry(valores_frame, "Valor Base:", valor_base_var, 0, 0, width=15)
        entry_base.bind('<KeyRelease>', lambda e: self.calcular_valores(tipo_nota))

        iva_var = tk.StringVar(value="0.00")
        setattr(self, f'iva_{tipo_nota}_var', iva_var)
        entry_iva = self.crear_entry(valores_frame, "% IVA:", iva_var, 0, 2, width=10)
        entry_iva.bind('<KeyRelease>', lambda e: self.calcular_valores(tipo_nota))

        valor_iva_var = tk.StringVar(value="0.00")
        setattr(self, f'valor_iva_{tipo_nota}_var', valor_iva_var)
        self.crear_entry_readonly(valores_frame, "Valor IVA:", valor_iva_var, 1, 0, width=15)

        porcentaje_retencion_var = tk.StringVar(value="0.00")
        setattr(self, f'porcentaje_retencion_{tipo_nota}_var', porcentaje_retencion_var)
        entry_porcentaje_retencion = self.crear_entry(valores_frame, "% Retención Renta:", porcentaje_retencion_var, 2, 0, width=10)
        entry_porcentaje_retencion.bind('<KeyRelease>', lambda e: self.calcular_valores(tipo_nota))

        valor_retencion_var = tk.StringVar(value="0.00")
        setattr(self, f'retencion_renta_{tipo_nota}_var', valor_retencion_var)
        self.crear_entry_readonly(valores_frame, "Valor Retención Renta:", valor_retencion_var, 2, 2, width=15)

        total_var = tk.StringVar(value="0.00")
        setattr(self, f'total_{tipo_nota}_var', total_var)
        self.crear_entry_readonly(valores_frame, "Total:", total_var, 1, 2, width=15)

        # Botones
        botones_frame = ttkb.Frame(parent)
        botones_frame.pack(fill=X, pady=10)

        self.crear_boton(
            botones_frame,
            text=f"Generar Nota {'Crédito' if tipo_nota == 'credito' else 'Débito'}",
            bootstyle=SUCCESS,
            command=lambda: self.generar_nota(tipo_nota)
        )
        self.crear_boton(
            botones_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=lambda: self.limpiar_formulario(tipo_nota)
        )
        self.crear_boton(
            botones_frame,
            text="Exportar XML",
            bootstyle=INFO,
            command=lambda: self.exportar_xml(tipo_nota),
            padx=(0, 0)
        )

    def setup_consultas_tab(self):
        """Configurar pestaña de consultas"""
        # Frame de filtros
        filtros_frame = ttkb.LabelFrame(self.tab_consultas, text="Filtros", padding=10)
        filtros_frame.pack(fill=X, pady=(0, 10))

        # Tipo de documento
        ttkb.Label(filtros_frame, text="Tipo:").grid(row=0, column=0, sticky=W)
        self.tipo_consulta_var = tk.StringVar(value="Todos")
        ttkb.Combobox(
            filtros_frame,
            textvariable=self.tipo_consulta_var,
            values=["Todos", "Nota Crédito", "Nota Débito"],
            width=15
        ).grid(row=0, column=1, padx=(5, 20))

        # Fechas (usar datetime ya importado globalmente)
        ttkb.Label(filtros_frame, text="Desde:").grid(row=0, column=2, sticky=W)
        self.fecha_desde_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttkb.Entry(filtros_frame, textvariable=self.fecha_desde_var, width=12).grid(row=0, column=3, padx=(5, 10))

        ttkb.Label(filtros_frame, text="Hasta:").grid(row=0, column=4, sticky=W)
        self.fecha_hasta_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttkb.Entry(filtros_frame, textvariable=self.fecha_hasta_var, width=12).grid(row=0, column=5, padx=(5, 20))

        # Botón buscar
        ttkb.Button(
            filtros_frame,
            text="Buscar",
            bootstyle=PRIMARY,
            command=self.buscar_notas
        ).grid(row=0, column=6)

        # Treeview para resultados
        self.tree = ttkb.Treeview(
            self.tab_consultas,
            columns=['numero', 'tipo', 'fecha', 'factura_ref', 'valor_total', 'estado'],
            show='headings',
            bootstyle=PRIMARY,
            height=15
        )

        # Configurar encabezados
        self.tree.heading('numero', text='Número', anchor=CENTER)
        self.tree.heading('tipo', text='Tipo', anchor=CENTER)
        self.tree.heading('fecha', text='Fecha', anchor=CENTER)
        self.tree.heading('factura_ref', text='Factura Ref.', anchor=CENTER)
        self.tree.heading('valor_total', text='Valor Total', anchor=CENTER)
        self.tree.heading('estado', text='Estado', anchor=CENTER)

        # Configurar columnas con alineación
        self.tree.column('numero', width=100, anchor=CENTER)
        self.tree.column('tipo', width=100, anchor=CENTER)
        self.tree.column('fecha', width=120, anchor=CENTER)
        self.tree.column('factura_ref', width=120, anchor=CENTER)
        self.tree.column('valor_total', width=120, anchor=E)  # Números a la derecha
        self.tree.column('estado', width=100, anchor=CENTER)

        self.tree.pack(fill=BOTH, expand=True, pady=(0, 10))

        # Scrollbar
        scrollbar = ttkb.Scrollbar(self.tab_consultas, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def connect_database(self):
        """Conectar a la base de datos"""
        if not self.db.connect():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        # Crear tablas si no existen
        self.crear_tablas()

    def crear_tablas(self):
        """Crear tablas necesarias"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS notas_credito_debito (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero VARCHAR(50) NOT NULL UNIQUE,
            tipo ENUM('credito', 'debito') NOT NULL,
            fecha_emision DATE NOT NULL,
            hora_emision TIME NOT NULL,
            factura_referencia VARCHAR(50) NOT NULL,
            codigo_concepto VARCHAR(50) NOT NULL,
            descripcion_concepto TEXT,
            valor_base DECIMAL(15,2) NOT NULL,
            porcentaje_iva DECIMAL(5,2) NOT NULL,
            valor_iva DECIMAL(15,2) NOT NULL,
            porcentaje_retencion DECIMAL(15,2) DEFAULT 0.00,
            retencion_renta DECIMAL(15,2) DEFAULT 0.00,
            valor_total DECIMAL(15,2) NOT NULL,
            cufe VARCHAR(200),
            xml_content LONGTEXT,
            estado ENUM('borrador', 'generado', 'enviado') DEFAULT 'borrador',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            numero_factura_ref VARCHAR(50),
            fecha_emision_ref DATE,
            nit_emisor_ref VARCHAR(50),
            razon_social_ref VARCHAR(255),
            total_bruto_factura_ref DECIMAL(15,2)
        )
        """

        self.db.execute_query(create_table_query)

    def obtener_valor_decimal(self, var, default='0.00'):
        """Devuelve el valor decimal de un StringVar, o un valor por defecto si no es válido."""
        try:
            return Decimal(var.get() or default)
        except Exception:
            return Decimal(default)

    def calcular_valores(self, tipo_nota):
        """Calcular valores de IVA, retención y total."""
        try:
            base = self.obtener_valor_decimal(getattr(self, f'valor_base_{tipo_nota}_var'))
            porcentaje_iva = self.obtener_valor_decimal(getattr(self, f'iva_{tipo_nota}_var'))
            porcentaje_retencion = self.obtener_valor_decimal(getattr(self, f'porcentaje_retencion_{tipo_nota}_var'))

            valor_iva = (base * porcentaje_iva / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            valor_retencion = (base * porcentaje_retencion / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total = base + valor_iva - valor_retencion

            getattr(self, f'valor_iva_{tipo_nota}_var').set(f"{valor_iva:.2f}")
            getattr(self, f'retencion_renta_{tipo_nota}_var').set(f"{valor_retencion:.2f}")
            getattr(self, f'total_{tipo_nota}_var').set(f"{total:.2f}")

        except Exception as e:
            logger.error(f"Error calculando valores: {e}")
            messagebox.showerror("Error", "Verifique los valores ingresados.")

    def generar_nota(self, tipo_nota):
        """
        Genera una nota crédito o débito, recopilando los datos del formulario,
        validándolos, generando el CUFE y guardando la información en la base de datos.
        """
        try:
            # Validación previa
            numero = getattr(self, f'numero_{tipo_nota}_var').get().strip()
            if not numero:
                messagebox.showerror("Error de Validación", "El número de la nota es obligatorio.")
                return
            fecha_emision = getattr(self, f'fecha_{tipo_nota}_var').get().strip()
            factura_referencia = getattr(self, f'factura_ref_{tipo_nota}_var').get().strip()
            codigo_concepto = getattr(self, f'codigo_concepto_{tipo_nota}_var').get().strip()
            descripcion_concepto = getattr(self, f'descripcion_{tipo_nota}_text').get('1.0', tk.END).strip()

            if not fecha_emision or not factura_referencia or not codigo_concepto or not descripcion_concepto:
                messagebox.showerror("Error de Validación", "Todos los campos obligatorios deben estar completos.")
                return

            ahora = datetime.now()
            hora_actual = ahora.strftime('%H:%M:%S')

            nota = NotaCreditoDebito(tipo_nota)
            nota.datos['numero'] = numero
            nota.datos['fecha_emision'] = fecha_emision
            nota.datos['factura_referencia'] = factura_referencia
            nota.datos['codigo_concepto'] = codigo_concepto
            nota.datos['descripcion_concepto'] = descripcion_concepto
            nota.datos['valor_base'] = self.obtener_valor_decimal(getattr(self, f'valor_base_{tipo_nota}_var'))
            nota.datos['porcentaje_iva'] = self.obtener_valor_decimal(getattr(self, f'iva_{tipo_nota}_var'))
            nota.datos['valor_iva'] = self.obtener_valor_decimal(getattr(self, f'valor_iva_{tipo_nota}_var'))
            nota.datos['porcentaje_retencion'] = self.obtener_valor_decimal(getattr(self, f'porcentaje_retencion_{tipo_nota}_var'))
            nota.datos['retencion_renta'] = self.obtener_valor_decimal(getattr(self, f'retencion_renta_{tipo_nota}_var'))
            nota.datos['valor_total'] = self.obtener_valor_decimal(getattr(self, f'total_{tipo_nota}_var'))

            # Validar datos
            valido, mensaje = nota.validar_datos()
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return

            # Generar CUFE
            nota.generar_cufe()

            # Guardar en base de datos
            query = """
            INSERT INTO notas_credito_debito
            (numero, tipo, fecha_emision, hora_emision, factura_referencia,
             codigo_concepto, descripcion_concepto, valor_base, porcentaje_iva,
             valor_iva, retencion_renta, porcentaje_retencion, valor_total, cufe, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            params = (
                nota.datos['numero'],
                tipo_nota,
                nota.datos['fecha_emision'],
                hora_actual,
                nota.datos['factura_referencia'],
                nota.datos['codigo_concepto'],
                nota.datos['descripcion_concepto'],
                float(nota.datos['valor_base']),
                float(nota.datos['porcentaje_iva']),
                float(nota.datos['valor_iva']),
                float(nota.datos['porcentaje_retencion']),
                float(nota.datos['retencion_renta']),
                float(nota.datos['valor_total']),
                nota.datos['cufe'],
                'generado'
            )

            if self.db.execute_query(query, params):
                messagebox.showinfo(
                    "Éxito",
                    f"Nota {'Crédito' if tipo_nota == 'credito' else 'Débito'} generada exitosamente\n"
                    f"CUFE: {nota.datos['cufe'][:20]}..."
                )
                self.limpiar_formulario(tipo_nota)
            else:
                messagebox.showerror("Error", "No se pudo guardar la nota")

        except Exception as e:
            logger.error(f"Error generando nota: {e}")
            messagebox.showerror("Error", f"Error generando nota: {str(e)}")

    def exportar_xml(self, tipo_nota):
        """Exportar nota como XML"""
        numero = getattr(self, f'numero_{tipo_nota}_var').get()
        if not numero:
            messagebox.showwarning("Advertencia", "Primero debe generar la nota")
            return

        # Buscar nota en BD
        query = "SELECT * FROM notas_credito_debito WHERE numero = %s AND tipo = %s"
        resultados = self.db.fetch_all(query, (numero, tipo_nota))

        if not resultados:
            messagebox.showwarning("Advertencia", "Nota no encontrada")
            return

        datos_nota = resultados[0]

        # Crear objeto nota
        nota = NotaCreditoDebito(tipo_nota)
        nota.datos.update({
            'numero': datos_nota['numero'],
            'fecha_emision': str(datos_nota['fecha_emision']),
            'hora_emision': str(datos_nota['hora_emision']),
            'factura_referencia': datos_nota['factura_referencia'],
            'codigo_concepto': datos_nota['codigo_concepto'],
            'descripcion_concepto': datos_nota['descripcion_concepto'],
            'valor_base': datos_nota['valor_base'],
            'porcentaje_iva': datos_nota['porcentaje_iva'],
            'valor_iva': datos_nota['valor_iva'],
            'valor_total': datos_nota['valor_total'],
            'cufe': datos_nota['cufe']
        })

        # Generar XML
        generador = GeneradorXML(nota)
        xml_content = generador.generar_xml()

        # Guardar archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            initialname=f"{'NC' if tipo_nota == 'credito' else 'ND'}_{numero}.xml"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(xml_content)

                # Actualizar BD con contenido XML
                update_query = "UPDATE notas_credito_debito SET xml_content = %s WHERE numero = %s"
                self.db.execute_query(update_query, (xml_content, numero))

                messagebox.showinfo("Éxito", f"XML exportado a: {filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Error exportando XML: {str(e)}")

    def limpiar_formulario(self, tipo_nota):
        """Limpiar formulario"""
        getattr(self, f'numero_{tipo_nota}_var').set('')
        getattr(self, f'factura_ref_{tipo_nota}_var').set('')
        getattr(self, f'codigo_concepto_{tipo_nota}_var').set('')
        getattr(self, f'descripcion_{tipo_nota}_text').delete('1.0', tk.END)
        getattr(self, f'valor_base_{tipo_nota}_var').set('0.00')
        getattr(self, f'iva_{tipo_nota}_var').set('0.00')
        getattr(self, f'valor_iva_{tipo_nota}_var').set('0.00')
        getattr(self, f'porcentaje_retencion_{tipo_nota}_var').set('0.50')
        getattr(self, f'retencion_renta_{tipo_nota}_var').set('0.00')
        getattr(self, f'total_{tipo_nota}_var').set('0.00')

    def buscar_notas(self):
        """Buscar notas en la base de datos"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Construir consulta
        query = """
        SELECT numero, tipo, fecha_emision, factura_referencia,
               valor_total, estado
        FROM notas_credito_debito
        WHERE fecha_emision BETWEEN %s AND %s
        """

        params = [self.fecha_desde_var.get(), self.fecha_hasta_var.get()]

        # Filtro por tipo
        if self.tipo_consulta_var.get() != "Todos":
            tipo_filtro = "credito" if self.tipo_consulta_var.get() == "Nota Crédito" else "debito"
            query += " AND tipo = %s"
            params.append(tipo_filtro)

        query += " ORDER BY fecha_emision DESC, numero DESC"

        # Ejecutar consulta
        resultados = self.db.fetch_all(query, params)

        # Mostrar resultados
        for nota in resultados:
            tipo_display = "Nota Crédito" if nota['tipo'] == 'credito' else "Nota Débito"
            self.tree.insert('', 'end', values=(
                nota['numero'],
                tipo_display,
                nota['fecha_emision'],
                nota['factura_referencia'],
                f"${nota['valor_total']:,.2f}",
                nota['estado'].title()
            ))

        if not resultados:
            messagebox.showinfo("Información", "No se encontraron registros")

    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()

    def __del__(self):
        """Destructor - cerrar conexión BD"""
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()

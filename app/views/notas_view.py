import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from datetime import datetime
from typing import Optional
from app.controllers.notas_controller import NotasController

class InterfazNotas:
    def __init__(self, controller: Optional[NotasController] = None):
        self.controller: Optional[NotasController] = controller
        self.root = ttkb.Window(themename="litera")
        self.root.title("Módulo Notas Crédito y Débito - DIAN")
        
        # Autoajustar al tamaño de la pantalla
        self.autoajustar_ventana()
        
        self.setup_ui()

    def autoajustar_ventana(self):
        """Autoajusta la ventana al tamaño de la pantalla"""
        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular el tamaño de la ventana (100% del tamaño de la pantalla)
        window_width = int(screen_width * 1.0)
        window_height = int(screen_height * 1.0)
        
        # Calcular la posición para centrar la ventana
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        # Configurar la geometría de la ventana
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Opcional: hacer que la ventana sea redimensionable
        self.root.resizable(True, True)

    def setup_ui(self):
        self.factura_ref_vars = {}
        self.entry_factura_refs = {}
        self.fecha_emision_vars = {}
        self.nit_emisor_vars = {}
        self.raz_soc_emisor_vars = {}
        self.total_bruto_vars = {}
        # Variables específicas por pestaña
        self.numero_vars = {}
        self.codigo_concepto_vars = {}
        self.descripcion_texts = {}
        self.valor_base_vars = {}
        self.iva_vars = {}
        self.valor_iva_vars = {}
        self.porcentaje_retencion_vars = {}
        self.retencion_renta_vars = {}
        self.total_vars = {}
        main_frame = ttkb.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttkb.Label(
            main_frame,
            text="Módulo Notas Crédito y Débito - DIAN",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        self.notebook = ttkb.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

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

    # Métodos de creación de widgets (copiados/adaptados de gui_fix_v5.py)
    def crear_boton(self, parent, text, command, bootstyle=PRIMARY, row=0, column=0, padx=(0, 10)):
        btn = ttkb.Button(parent, text=text, bootstyle=bootstyle, command=command)
        btn.grid(row=row, column=column, padx=padx)
        return btn

    def crear_entry(self, parent, label, var, row, column, width=15, pady=(0, 10)):
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.W, pady=(0, 2))
        entry = ttkb.Entry(parent, textvariable=var, width=width)
        entry.grid(row=row+1, column=column, padx=(5, 20), pady=pady, sticky=tk.EW)
        return entry

    def crear_entry_readonly(self, parent, label, var, row, column, width=15):
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.W, pady=(5, 0))
        entry = ttkb.Entry(parent, textvariable=var, width=width, state=READONLY)
        entry.grid(row=row+1, column=column, padx=(5, 20), pady=(5, 0))
        return entry

    def crear_combobox(self, parent, label, var, values, row, column, width=40):
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.W)
        combo = ttkb.Combobox(parent, textvariable=var, values=values, width=width)
        combo.grid(row=row+1, column=column, padx=(5, 0))
        return combo

    def crear_text_multilinea(self, parent, label, row, column, width=50, height=3, pady=(0, 10)):
        ttkb.Label(parent, text=label).grid(row=row, column=column, sticky=tk.NW, pady=(0, 2))
        text_widget = tk.Text(parent, height=height, width=width)
        text_widget.grid(row=row+1, column=column, padx=(5, 0), pady=pady, sticky=tk.EW)
        return text_widget

    def crear_labelframe(self, parent, text, padding=10):
        frame = ttkb.LabelFrame(parent, text=text, padding=padding)
        frame.pack(fill=tk.X, pady=(0, 10))
        return frame

    def setup_nota_tab(self, parent, tipo_nota):
        print(f"Creando widgets en pestaña: {tipo_nota}")
        # Crear canvas y scrollbar para scroll vertical
        canvas = tk.Canvas(parent)
        scrollbar = ttkb.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttkb.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- NUEVO: Tipo de Operación ---
        if not hasattr(self, 'tipo_operacion_vars'):
            self.tipo_operacion_vars = {}
        if tipo_nota == 'credito':
            tipo_operacion_values = [
                "20 - Nota Crédito que referencia una factura electrónica",
                "22 - Nota Crédito sin referencia a facturas"
            ]
            default_tipo_operacion = tipo_operacion_values[0]
        else:
            tipo_operacion_values = [
                "30 - Nota Débito que referencia una factura electrónica",
                "32 - Nota Débito sin referencia a facturas"
            ]
            default_tipo_operacion = tipo_operacion_values[0]
        self.tipo_operacion_vars[tipo_nota] = tk.StringVar(value=default_tipo_operacion)
        tipo_operacion_frame = self.crear_labelframe(scrollable_frame, "Tipo de Operación")
        self.crear_combobox(
            tipo_operacion_frame,
            "Tipo de Operación:",
            self.tipo_operacion_vars[tipo_nota],
            tipo_operacion_values,
            0, 0, width=50
        )
        # --- FIN NUEVO ---

        datos_frame = self.crear_labelframe(scrollable_frame, "Datos Básicos")
        self.numero_vars[tipo_nota] = tk.StringVar()
        self.crear_entry(datos_frame, "Número:", self.numero_vars[tipo_nota], 0, 0, width=20)
        self.fecha_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(datos_frame, "Fecha:", self.fecha_var, 0, 1, width=15)

        referencias_frame = self.crear_labelframe(scrollable_frame, "Referencias del documento")
        self.factura_ref_vars[tipo_nota] = tk.StringVar()
        self.entry_factura_refs[tipo_nota] = self.crear_entry(referencias_frame, "Factura Referencia:", self.factura_ref_vars[tipo_nota], 0, 0, width=20)
        self.entry_factura_refs[tipo_nota].bind('<FocusOut>', lambda e, t=tipo_nota: self.root.after(500, lambda: self.on_factura_ref_change(t)))
        self.entry_factura_refs[tipo_nota].bind('<Return>', lambda e, t=tipo_nota: self.on_factura_ref_change(t))
        # Frame para los botones
        botones_frame = ttkb.Frame(parent)
        botones_frame.pack(fill=tk.X, pady=10)
        self.boton_buscar_factura = ttkb.Button(
            botones_frame,
            text="Buscar",
            command=lambda t=tipo_nota: self.on_factura_ref_change(t)
        )
        self.boton_buscar_factura.pack(side=tk.LEFT, padx=(0, 10))
        self.boton_limpiar = ttkb.Button(
            botones_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=lambda t=tipo_nota: self.limpiar_formulario(t),
        )
        self.boton_limpiar.pack(side=tk.LEFT, padx=(0, 10))
        self.boton_exportar = ttkb.Button(
            botones_frame,
            text="Exportar XML",
            bootstyle=INFO,
            command=self.exportar_xml
        )
        self.boton_exportar.pack(side=tk.LEFT, padx=(0, 10))
        self.boton_generar = ttkb.Button(
            botones_frame,
            text=f"Generar Nota {'Crédito' if tipo_nota == 'credito' else 'Débito'}",
            bootstyle=SUCCESS,
            command=self.on_generar_nota
        )
        self.boton_generar.pack(side=tk.LEFT, padx=(0, 10))
        self.fecha_emision_vars[tipo_nota] = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(referencias_frame, "Fecha de Emisión:", self.fecha_emision_vars[tipo_nota], 0, 1, width=15)
        self.nit_emisor_vars[tipo_nota] = tk.StringVar()
        self.crear_entry(referencias_frame, "Nit del Emisor:", self.nit_emisor_vars[tipo_nota], 0, 2, width=20)
        self.raz_soc_emisor_vars[tipo_nota] = tk.StringVar()
        self.crear_entry(referencias_frame, "Razón Social del Emisor:", self.raz_soc_emisor_vars[tipo_nota], 0, 3, width=40)
        self.total_bruto_vars[tipo_nota] = tk.StringVar(value="0.00")
        self.crear_entry(referencias_frame, "Total Bruto Factura:", self.total_bruto_vars[tipo_nota], 0, 4, width=15)

        concepto_frame = self.crear_labelframe(scrollable_frame, "Concepto De Corrección")
        self.codigo_concepto_vars[tipo_nota] = tk.StringVar()
        conceptos_nota_credito = [
            "1 - Devolución parcial de los bienes y/o no aceptación parcial del servicio",
            "2 - Anulación de factura electrónica",
            "3 - Rebaja o descuento parcial o total",
            "4 - Ajuste de precio",
            "5 - Descuento comercial por pronto pago",
            "6 - Descuento comercial por volumen de ventas",
            "7 - Otros"
        ]
        self.crear_combobox(concepto_frame, "Código Concepto:", self.codigo_concepto_vars[tipo_nota], conceptos_nota_credito, 0, 0, width=40)
        self.descripcion_texts[tipo_nota] = self.crear_text_multilinea(concepto_frame, "Descripción:", 2, 0, width=50, height=3)

        valores_frame = self.crear_labelframe(scrollable_frame, "Valores")
        for i in range(3):
            valores_frame.grid_columnconfigure(i, weight=1)

        bold_font = ("Arial", 10, "bold")
        entry_width = 15

        # Primera fila: Valor Base, % IVA, Valor IVA
        ttkb.Label(valores_frame, text="Valor Base:", font=bold_font).grid(row=0, column=0, sticky=tk.E, pady=(5, 2))
        ttkb.Label(valores_frame, text="% IVA:", font=bold_font).grid(row=0, column=1, sticky=tk.E, pady=(5, 2))
        ttkb.Label(valores_frame, text="Valor IVA:", font=bold_font).grid(row=0, column=2, sticky=tk.E, pady=(5, 2))
        self.valor_base_vars[tipo_nota] = tk.StringVar(value="0.00")
        entry_base = ttkb.Entry(valores_frame, textvariable=self.valor_base_vars[tipo_nota], width=entry_width, justify="center")
        entry_base.grid(row=1, column=0, padx=5, pady=2, sticky=tk.EW)
        self.iva_vars[tipo_nota] = tk.StringVar(value="0.00")
        entry_iva = ttkb.Entry(valores_frame, textvariable=self.iva_vars[tipo_nota], width=entry_width, justify="center")
        entry_iva.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)
        self.valor_iva_vars[tipo_nota] = tk.StringVar(value="0.00")
        entry_iva_read = ttkb.Entry(valores_frame, textvariable=self.valor_iva_vars[tipo_nota], width=entry_width, state="readonly", justify="center")
        entry_iva_read.grid(row=1, column=2, padx=5, pady=2, sticky=tk.EW)

        # Separador horizontal
        ttkb.Separator(valores_frame, orient="horizontal").grid(row=2, column=0, columnspan=3, sticky="ew", pady=8)

        # Segunda fila: % Retención Renta, Valor Retención Renta
        ttkb.Label(valores_frame, text="% Retención Renta:", font=bold_font).grid(row=3, column=0, sticky=tk.E, pady=(5, 2))
        ttkb.Label(valores_frame, text="Valor Retención Renta:", font=bold_font).grid(row=3, column=1, sticky=tk.E, pady=(5, 2))
        self.porcentaje_retencion_vars[tipo_nota] = tk.StringVar(value="0.00")
        entry_porcentaje_retencion = ttkb.Entry(valores_frame, textvariable=self.porcentaje_retencion_vars[tipo_nota], width=entry_width, justify="center")
        entry_porcentaje_retencion.grid(row=4, column=0, padx=5, pady=2, sticky=tk.EW)
        self.retencion_renta_vars[tipo_nota] = tk.StringVar(value="0.00")
        entry_retencion_read = ttkb.Entry(valores_frame, textvariable=self.retencion_renta_vars[tipo_nota], width=entry_width, state="readonly", justify="center")
        entry_retencion_read.grid(row=4, column=1, padx=5, pady=2, sticky=tk.EW)

        # Total en una fila aparte
        ttkb.Label(valores_frame, text="Total:", font=bold_font).grid(row=5, column=0, sticky=tk.E, pady=(10, 2))
        self.total_vars[tipo_nota] = tk.StringVar(value="0.00")
        entry_total_read = ttkb.Entry(valores_frame, textvariable=self.total_vars[tipo_nota], width=entry_width, state="readonly", justify="center")
        entry_total_read.grid(row=6, column=0, padx=5, pady=2, sticky=tk.EW)

        # Enlazar eventos de cálculo
        entry_base.bind('<KeyRelease>', lambda e, t=tipo_nota: self.calcular_valores(t))
        entry_iva.bind('<KeyRelease>', lambda e, t=tipo_nota: self.calcular_valores(t))
        entry_porcentaje_retencion.bind('<KeyRelease>', lambda e, t=tipo_nota: self.calcular_valores(t))

    def setup_consultas_tab(self):
        filtros_frame = self.crear_labelframe(self.tab_consultas, "Filtros")
        self.tipo_consulta_var = tk.StringVar(value="Todos")
        self.crear_combobox(filtros_frame, "Tipo:", self.tipo_consulta_var, ["Todos", "Nota Crédito", "Nota Débito"], 0, 0, width=15)
        self.fecha_desde_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(filtros_frame, "Desde:", self.fecha_desde_var, 0, 2, width=12)
        self.fecha_hasta_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(filtros_frame, "Hasta:", self.fecha_hasta_var, 0, 4, width=12)
        self.crear_boton(filtros_frame, "Buscar", self.buscar_notas, bootstyle=PRIMARY, row=0, column=6, padx=(0, 0))
        columns = ['numero', 'tipo', 'tipo_operacion', 'fecha', 'factura_ref', 'valor_total', 'estado']
        headings = ['Número', 'Tipo', 'Tipo Operación', 'Fecha', 'Factura Ref.', 'Valor Total', 'Estado']
        column_widths = [100, 100, 140, 120, 120, 120, 100]
        anchor_map = [tk.CENTER, tk.CENTER, tk.CENTER, tk.CENTER, tk.CENTER, tk.E, tk.CENTER]
        self.tree = self.crear_tabla_resultados(
            self.tab_consultas,
            columns=columns,
            headings=headings,
            column_widths=column_widths,
            anchor_map=anchor_map,
            height=15
        )
        self.crear_scrollbar_vertical(self.tab_consultas, self.tree)

    # Métodos stub para limpiar formulario y exportar XML
    def limpiar_formulario(self, tipo_nota=None):
        if tipo_nota is None:
            tipo_nota = self.notebook.tab(self.notebook.select(), "text").lower().replace(' ', '_').replace('nota_', '')
        # Limpiar campos principales
        self.numero_vars[tipo_nota].set("")
        # Limpiar referencias del documento
        self.factura_ref_vars[tipo_nota].set("")
        self.fecha_emision_vars[tipo_nota].set(datetime.now().strftime('%Y-%m-%d'))
        self.nit_emisor_vars[tipo_nota].set("")
        self.raz_soc_emisor_vars[tipo_nota].set("")
        self.total_bruto_vars[tipo_nota].set("0.00")
        # Limpiar otros campos si lo deseas
        self.codigo_concepto_vars[tipo_nota].set("")
        self.descripcion_texts[tipo_nota].delete('1.0', 'end')
        self.valor_base_vars[tipo_nota].set("0.00")
        self.iva_vars[tipo_nota].set("0.00")
        self.valor_iva_vars[tipo_nota].set("0.00")
        self.porcentaje_retencion_vars[tipo_nota].set("0.00")
        self.retencion_renta_vars[tipo_nota].set("0.00")
        self.total_vars[tipo_nota].set("0.00")

    def exportar_xml(self):
        # Implementa la lógica de exportar XML
        pass

    def calcular_valores(self, tipo_nota):
        try:
            base = float(self.valor_base_vars[tipo_nota].get() or '0')
            porcentaje_iva = float(self.iva_vars[tipo_nota].get() or '0')
            porcentaje_retencion = float(self.porcentaje_retencion_vars[tipo_nota].get() or '0')
            valor_iva = round(base * porcentaje_iva / 100, 2)
            valor_retencion = round(base * porcentaje_retencion / 100, 2)
            total = base + valor_iva - valor_retencion
            self.valor_iva_vars[tipo_nota].set(f"{valor_iva:.2f}")
            self.retencion_renta_vars[tipo_nota].set(f"{valor_retencion:.2f}")
            self.total_vars[tipo_nota].set(f"{total:.2f}")
        except Exception:
            pass

    def on_generar_nota(self):
        datos_formulario = self.obtener_datos_formulario()
        if self.controller is not None:
            self.controller.generar_nota(datos_formulario)

    def buscar_notas(self):
        filtros = self.obtener_filtros_consulta()
        if self.controller is not None:
            self.controller.consultar_notas(filtros)

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Información", mensaje)

    def mostrar_resultados(self, resultados):
        # Este método debe limpiar y poblar el treeview de resultados
        self.tree.delete(*self.tree.get_children())
        for nota in resultados:
            tipo_display = "Nota Crédito" if nota['tipo'] == 'credito' else "Nota Débito"
            tipo_operacion = nota.get('tipo_operacion', '')
            self.tree.insert('', 'end', values=(
                nota['numero'],
                tipo_display,
                tipo_operacion,
                nota['fecha_emision'],
                nota['factura_referencia'],
                f"${nota['valor_total']:,.2f}",
                nota['estado'].title()
            ))

    def obtener_datos_formulario(self):
        tipo_nota = self.notebook.tab(self.notebook.select(), "text").lower().replace(' ', '_').replace('nota_', '').replace('é', 'e')
        # Extraer solo el código de tipo_operacion (ej: '20', '22', '30', '32')
        tipo_operacion_full = self.tipo_operacion_vars[tipo_nota].get() if hasattr(self, 'tipo_operacion_vars') and tipo_nota in self.tipo_operacion_vars else None
        tipo_operacion = tipo_operacion_full.split(' - ')[0] if tipo_operacion_full else None
        return {
            "tipo_nota": tipo_nota,
            "tipo_operacion": tipo_operacion,
            "numero": self.numero_vars[tipo_nota].get(),
            "fecha_emision": self.fecha_emision_vars[tipo_nota].get(),
            "factura_referencia": self.factura_ref_vars[tipo_nota].get(),
            "nit_emisor": self.nit_emisor_vars[tipo_nota].get(),
            "razon_social_emisor": self.raz_soc_emisor_vars[tipo_nota].get(),
            "total_bruto": self.total_bruto_vars[tipo_nota].get(),
            "codigo_concepto": self.codigo_concepto_vars[tipo_nota].get(),
            "descripcion_concepto": self.descripcion_texts[tipo_nota].get('1.0', 'end').strip(),
            "valor_base": self.valor_base_vars[tipo_nota].get(),
            "porcentaje_iva": self.iva_vars[tipo_nota].get(),
            "valor_iva": self.valor_iva_vars[tipo_nota].get(),
            "porcentaje_retencion": self.porcentaje_retencion_vars[tipo_nota].get(),
            "retencion_renta": self.retencion_renta_vars[tipo_nota].get(),
            "valor_total": self.total_vars[tipo_nota].get(),
        }

    def obtener_filtros_consulta(self):
        # Devuelve un dict con los filtros de la UI
        return {
            "tipo": self.tipo_consulta_var.get(),
            "fecha_desde": self.fecha_desde_var.get(),
            "fecha_hasta": self.fecha_hasta_var.get(),
        }

    def crear_tabla_resultados(self, parent, columns, headings, column_widths, anchor_map, height=15):
        tree = ttkb.Treeview(
            parent,
            columns=columns,
            show='headings',
            height=height
        )
        for col, head, width, anchor in zip(columns, headings, column_widths, anchor_map):
            tree.heading(col, text=head, anchor=anchor)
            tree.column(col, width=width, anchor=anchor)
        tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        return tree

    def crear_scrollbar_vertical(self, parent, widget, side=tk.RIGHT):
        scrollbar = ttkb.Scrollbar(parent, orient=tk.VERTICAL, command=widget.yview)
        widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=side, fill=tk.Y)
        return scrollbar 

    def on_factura_ref_change(self, tipo_nota):
        entry = self.entry_factura_refs[tipo_nota]
        var = self.factura_ref_vars[tipo_nota]
        var.set(entry.get())
        numero = var.get().strip()
        resultado = self.controller.buscar_factura_por_numero(numero)
        if resultado:
            if not isinstance(resultado, dict):
                campos = [
                    'id', 'numero_documento', 'razon_social', 'numero_factura', 'subtotal_factura', 'iva', 'ic', 'inc', 'ica', 'rete_fuente',
                    'fecha_recepcion', 'fecha_emision', 'fecha_vencimiento', 'total_retenciones', 'total_factura', 'tipo_cliente',
                    'periodo_factura', 'notas_finales', 'created_at', 'updated_at'
                ]
                resultado = dict(zip(campos, resultado))
            self.fecha_emision_vars[tipo_nota].set(str(resultado.get('fecha_emision', '')))
            self.nit_emisor_vars[tipo_nota].set(str(resultado.get('numero_documento', '')))
            self.raz_soc_emisor_vars[tipo_nota].set(str(resultado.get('razon_social', '')))
            self.total_bruto_vars[tipo_nota].set(str(resultado.get('total_factura', '0.00')))
        else:
            self.mostrar_mensaje('Factura no encontrada') 
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
        self.root.geometry("1200x800")
        self.setup_ui()

    def setup_ui(self):
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

        # Ahora, usa scrollable_frame como parent para el contenido del formulario
        datos_frame = self.crear_labelframe(scrollable_frame, "Datos Básicos")
        self.numero_var = tk.StringVar()
        self.crear_entry(datos_frame, "Número:", self.numero_var, 0, 0, width=20)
        self.fecha_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(datos_frame, "Fecha:", self.fecha_var, 0, 1, width=15)

        referencias_frame = self.crear_labelframe(scrollable_frame, "Referencias del documento")
        self.factura_ref_var = tk.StringVar()
        entry_factura_ref = self.crear_entry(referencias_frame, "Factura Referencia:", self.factura_ref_var, 0, 0, width=20)
        entry_factura_ref.bind('<FocusOut>', self.on_factura_ref_change)
        entry_factura_ref.bind('<Return>', self.on_factura_ref_change)
        self.fecha_emision_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(referencias_frame, "Fecha de Emisión:", self.fecha_emision_var, 0, 1, width=15)
        self.nit_emisor_var = tk.StringVar()
        self.crear_entry(referencias_frame, "Nit del Emisor:", self.nit_emisor_var, 0, 2, width=20)
        self.raz_soc_emisor_var = tk.StringVar()
        self.crear_entry(referencias_frame, "Razón Social del Emisor:", self.raz_soc_emisor_var, 0, 3, width=40)
        self.total_bruto_var = tk.StringVar(value="0.00")
        self.crear_entry(referencias_frame, "Total Bruto Factura:", self.total_bruto_var, 0, 4, width=15)

        concepto_frame = self.crear_labelframe(scrollable_frame, "Concepto De Corrección")
        self.codigo_concepto_var = tk.StringVar()
        conceptos_nota_credito = [
            "1 - Devolución parcial de los bienes y/o no aceptación parcial del servicio",
            "2 - Anulación de factura electrónica",
            "3 - Rebaja o descuento parcial o total",
            "4 - Ajuste de precio",
            "5 - Descuento comercial por pronto pago",
            "6 - Descuento comercial por volumen de ventas",
            "7 - Otros"
        ]
        self.crear_combobox(concepto_frame, "Código Concepto:", self.codigo_concepto_var, conceptos_nota_credito, 0, 0, width=40)
        self.descripcion_text = self.crear_text_multilinea(concepto_frame, "Descripción:", 2, 0, width=50, height=3)

        valores_frame = self.crear_labelframe(scrollable_frame, "Valores")
        valores_frame.grid_columnconfigure(0, weight=1)

        row = 0
        self.valor_base_var = tk.StringVar(value="0.00")
        entry_base = self.crear_entry(valores_frame, "Valor Base:", self.valor_base_var, row, 0)
        row += 2
        self.iva_var = tk.StringVar(value="0.00")
        entry_iva = self.crear_entry(valores_frame, "% IVA:", self.iva_var, row, 0)
        row += 2
        self.valor_iva_var = tk.StringVar(value="0.00")
        self.crear_entry_readonly(valores_frame, "Valor IVA:", self.valor_iva_var, row, 0)
        self.porcentaje_retencion_var = tk.StringVar(value="0.00")
        entry_porcentaje_retencion = self.crear_entry(valores_frame, "% Retención Renta:", self.porcentaje_retencion_var, 6, 0, width=10)
        self.retencion_renta_var = tk.StringVar(value="0.00")
        self.crear_entry_readonly(valores_frame, "Valor Retención Renta:", self.retencion_renta_var, 8, 0, width=15)
        self.total_var = tk.StringVar(value="0.00")
        self.crear_entry_readonly(valores_frame, "Total:", self.total_var, 10, 0, width=15)

        # Enlazar eventos de cálculo
        entry_base.bind('<KeyRelease>', lambda e: self.calcular_valores())
        entry_iva.bind('<KeyRelease>', lambda e: self.calcular_valores())
        entry_porcentaje_retencion.bind('<KeyRelease>', lambda e: self.calcular_valores())

        # Botones
        botones_frame = ttkb.Frame(scrollable_frame)
        botones_frame.pack(fill=tk.X, pady=10)
        self.crear_boton(
            botones_frame,
            text=f"Generar Nota {'Crédito' if tipo_nota == 'credito' else 'Débito'}",
            bootstyle=SUCCESS,
            command=self.on_generar_nota,
            row=0, column=0
        )
        self.crear_boton(
            botones_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.limpiar_formulario,
            row=0, column=1
        )
        self.crear_boton(
            botones_frame,
            text="Exportar XML",
            bootstyle=INFO,
            command=self.exportar_xml,
            row=0, column=2, padx=(0, 0)
        )

    def setup_consultas_tab(self):
        filtros_frame = self.crear_labelframe(self.tab_consultas, "Filtros")
        self.tipo_consulta_var = tk.StringVar(value="Todos")
        self.crear_combobox(filtros_frame, "Tipo:", self.tipo_consulta_var, ["Todos", "Nota Crédito", "Nota Débito"], 0, 0, width=15)
        self.fecha_desde_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(filtros_frame, "Desde:", self.fecha_desde_var, 0, 2, width=12)
        self.fecha_hasta_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.crear_entry(filtros_frame, "Hasta:", self.fecha_hasta_var, 0, 4, width=12)
        self.crear_boton(filtros_frame, "Buscar", self.buscar_notas, bootstyle=PRIMARY, row=0, column=6, padx=(0, 0))
        columns = ['numero', 'tipo', 'fecha', 'factura_ref', 'valor_total', 'estado']
        headings = ['Número', 'Tipo', 'Fecha', 'Factura Ref.', 'Valor Total', 'Estado']
        column_widths = [100, 100, 120, 120, 120, 100]
        anchor_map = [tk.CENTER, tk.CENTER, tk.CENTER, tk.CENTER, tk.E, tk.CENTER]
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
    def limpiar_formulario(self):
        # Implementa la lógica de limpiar los campos del formulario
        pass

    def exportar_xml(self):
        # Implementa la lógica de exportar XML
        pass

    def calcular_valores(self):
        try:
            base = float(self.valor_base_var.get() or '0')
            porcentaje_iva = float(self.iva_var.get() or '0')
            porcentaje_retencion = float(self.porcentaje_retencion_var.get() or '0')
            valor_iva = round(base * porcentaje_iva / 100, 2)
            valor_retencion = round(base * porcentaje_retencion / 100, 2)
            total = base + valor_iva - valor_retencion
            self.valor_iva_var.set(f"{valor_iva:.2f}")
            self.retencion_renta_var.set(f"{valor_retencion:.2f}")
            self.total_var.set(f"{total:.2f}")
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
            self.tree.insert('', 'end', values=(
                nota['numero'],
                tipo_display,
                nota['fecha_emision'],
                nota['factura_referencia'],
                f"${nota['valor_total']:,.2f}",
                nota['estado'].title()
            ))

    def obtener_datos_formulario(self):
        # Devuelve un dict con los datos del formulario
        # Debes adaptar esto a tus widgets reales
        return {
            "tipo_nota": self.tipo_nota_var.get(),
            "numero": self.numero_var.get(),
            "fecha_emision": self.fecha_var.get(),
            "factura_referencia": self.factura_ref_var.get(),
            "codigo_concepto": self.codigo_concepto_var.get(),
            "descripcion_concepto": self.descripcion_text.get('1.0', 'end').strip(),
            "valor_base": self.valor_base_var.get(),
            "porcentaje_iva": self.iva_var.get(),
            "valor_iva": self.valor_iva_var.get(),
            "porcentaje_retencion": self.porcentaje_retencion_var.get(),
            "retencion_renta": self.retencion_renta_var.get(),
            "valor_total": self.total_var.get(),
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

    def on_factura_ref_change(self, event=None):
        if not self.controller:
            return
        numero = self.factura_ref_var.get().strip()
        if not numero:
            return
        datos_factura = dict(self.controller.buscar_factura_por_numero(numero))
        if datos_factura:
            self.fecha_emision_var.set(str(datos_factura.get('fecha_emision', '')))
            self.nit_emisor_var.set(str(datos_factura.get('numero_documento', '')))
            self.raz_soc_emisor_var.set(str(datos_factura.get('razon_social', '')))
            self.total_bruto_var.set(str(datos_factura.get('total_factura', '0.00')))
        else:
            self.mostrar_mensaje('Factura no encontrada') 
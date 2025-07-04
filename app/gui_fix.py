"""Módulo: InterfazNotas"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import logging

from app.database import DatabaseManager
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
        
    def setup_nota_tab(self, parent, tipo_nota):
        """Configurar pestaña de nota"""
        # Frame de datos básicos
        datos_frame = ttkb.LabelFrame(parent, text="Datos Básicos", padding=10)
        datos_frame.pack(fill=X, pady=(0, 10))
        
        # Número de nota
        ttkb.Label(datos_frame, text="Número:").grid(row=0, column=0, sticky=W, padx=(0, 5))
        numero_var = tk.StringVar()
        setattr(self, f'numero_{tipo_nota}_var', numero_var)
        ttkb.Entry(datos_frame, textvariable=numero_var, width=20).grid(row=0, column=1, padx=(0, 20))
        
        # Fecha
        ttkb.Label(datos_frame, text="Fecha:").grid(row=0, column=2, sticky=W, padx=(0, 5))
        fecha_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        setattr(self, f'fecha_{tipo_nota}_var', fecha_var)
        ttkb.Entry(datos_frame, textvariable=fecha_var, width=15).grid(row=0, column=3)
        
        # Factura referencia
        ttkb.Label(datos_frame, text="Factura Referencia:").grid(row=1, column=0, sticky=W, padx=(0, 5))
        factura_ref_var = tk.StringVar()
        setattr(self, f'factura_ref_{tipo_nota}_var', factura_ref_var)
        ttkb.Entry(datos_frame, textvariable=factura_ref_var, width=20).grid(row=1, column=1, pady=(5, 0))
        
        # Concepto
        concepto_frame = ttkb.LabelFrame(parent, text="Concepto", padding=10)
        concepto_frame.pack(fill=X, pady=(0, 10))
        
        ttkb.Label(concepto_frame, text="Código Concepto:").grid(row=0, column=0, sticky=W)
        codigo_concepto_var = tk.StringVar()
        setattr(self, f'codigo_concepto_{tipo_nota}_var', codigo_concepto_var)
        
        # Combobox con conceptos DIAN
        conceptos = [
            "1 - Devolución parcial de los bienes",
            "2 - Anulación de la operación",
            "3 - Rebaja total aplicada",
            "4 - Descuento total aplicado",
            "5 - Rescisión de la operación",
            "6 - Otros"
        ]
        
        combo_concepto = ttkb.Combobox(
            concepto_frame, 
            textvariable=codigo_concepto_var,
            values=conceptos,
            width=40
        )
        combo_concepto.grid(row=0, column=1, padx=(5, 0))
        
        # Descripción
        ttkb.Label(concepto_frame, text="Descripción:").grid(row=1, column=0, sticky=NW, pady=(5, 0))
        descripcion_var = tk.StringVar()
        setattr(self, f'descripcion_{tipo_nota}_var', descripcion_var)
        
        descripcion_text = tk.Text(concepto_frame, height=3, width=50)
        descripcion_text.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))
        setattr(self, f'descripcion_{tipo_nota}_text', descripcion_text)
        
        # Valores
        valores_frame = ttkb.LabelFrame(parent, text="Valores", padding=10)
        valores_frame.pack(fill=X, pady=(0, 10))
        
        # Valor base
        ttkb.Label(valores_frame, text="Valor Base:").grid(row=0, column=0, sticky=W)
        valor_base_var = tk.StringVar(value="0.00")
        setattr(self, f'valor_base_{tipo_nota}_var', valor_base_var)
        entry_base = ttkb.Entry(valores_frame, textvariable=valor_base_var, width=15)
        entry_base.grid(row=0, column=1, padx=(5, 20))
        entry_base.bind('<KeyRelease>', lambda e: self.calcular_valores(tipo_nota))
        
        # IVA
        ttkb.Label(valores_frame, text="% IVA:").grid(row=0, column=2, sticky=W)
        iva_var = tk.StringVar(value="19.00")
        setattr(self, f'iva_{tipo_nota}_var', iva_var)
        entry_iva = ttkb.Entry(valores_frame, textvariable=iva_var, width=10)
        entry_iva.grid(row=0, column=3, padx=(5, 20))
        entry_iva.bind('<KeyRelease>', lambda e: self.calcular_valores(tipo_nota))
        
        # Valor IVA
        ttkb.Label(valores_frame, text="Valor IVA:").grid(row=1, column=0, sticky=W, pady=(5, 0))
        valor_iva_var = tk.StringVar(value="0.00")
        setattr(self, f'valor_iva_{tipo_nota}_var', valor_iva_var)
        ttkb.Entry(valores_frame, textvariable=valor_iva_var, width=15, state=READONLY).grid(
            row=1, column=1, padx=(5, 20), pady=(5, 0)
        )
        
        # Total
        ttkb.Label(valores_frame, text="Total:").grid(row=1, column=2, sticky=W, pady=(5, 0))
        total_var = tk.StringVar(value="0.00")
        setattr(self, f'total_{tipo_nota}_var', total_var)
        ttkb.Entry(valores_frame, textvariable=total_var, width=15, state=READONLY).grid(
            row=1, column=3, padx=(5, 0), pady=(5, 0)
        )
        
        # Botones
        botones_frame = ttkb.Frame(parent)
        botones_frame.pack(fill=X, pady=10)
        
        ttkb.Button(
            botones_frame,
            text=f"Generar Nota {'Crédito' if tipo_nota == 'credito' else 'Débito'}",
            bootstyle=SUCCESS,
            command=lambda: self.generar_nota(tipo_nota)
        ).pack(side=LEFT, padx=(0, 10))
        
        ttkb.Button(
            botones_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=lambda: self.limpiar_formulario(tipo_nota)
        ).pack(side=LEFT, padx=(0, 10))
        
        ttkb.Button(
            botones_frame,
            text="Exportar XML",
            bootstyle=INFO,
            command=lambda: self.exportar_xml(tipo_nota)
        ).pack(side=LEFT)
    
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
        
        # Fechas
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
            columns=('numero', 'tipo', 'fecha', 'factura_ref', 'valor_total', 'estado'),
            show='headings',
            height=15
        )
        
        # Configurar columnas
        self.tree.heading('numero', text='Número')
        self.tree.heading('tipo', text='Tipo')
        self.tree.heading('fecha', text='Fecha')
        self.tree.heading('factura_ref', text='Factura Ref.')
        self.tree.heading('valor_total', text='Valor Total')
        self.tree.heading('estado', text='Estado')
        
        self.tree.column('numero', width=100)
        self.tree.column('tipo', width=100)
        self.tree.column('fecha', width=100)
        self.tree.column('factura_ref', width=120)
        self.tree.column('valor_total', width=100)
        self.tree.column('estado', width=80)
        
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
            codigo_concepto VARCHAR(10) NOT NULL,
            descripcion_concepto TEXT,
            valor_base DECIMAL(15,2) NOT NULL,
            porcentaje_iva DECIMAL(5,2) NOT NULL,
            valor_iva DECIMAL(15,2) NOT NULL,
            valor_total DECIMAL(15,2) NOT NULL,
            cufe VARCHAR(200),
            xml_content LONGTEXT,
            estado ENUM('borrador', 'generado', 'enviado') DEFAULT 'borrador',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        self.db.execute_query(create_table_query)
    
    def calcular_valores(self, tipo_nota):
        """Calcular valores de IVA y total"""
        try:
            valor_base_var = getattr(self, f'valor_base_{tipo_nota}_var')
            iva_var = getattr(self, f'iva_{tipo_nota}_var')
            valor_iva_var = getattr(self, f'valor_iva_{tipo_nota}_var')
            total_var = getattr(self, f'total_{tipo_nota}_var')
            
            base = Decimal(valor_base_var.get() or '0')
            porcentaje = Decimal(iva_var.get() or '0')
            
            valor_iva = (base * porcentaje / 100).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            total = base + valor_iva
            
            valor_iva_var.set(f"{valor_iva:.2f}")
            total_var.set(f"{total:.2f}")
            
        except (ValueError, Exception) as e:
            logger.error(f"Error calculando valores: {e}")
    
    def generar_nota(self, tipo_nota):
        """Generar nota crédito o débito"""
        try:
            # Obtener la fecha y hora actual
            ahora = datetime.now()
            fecha_actual = ahora.strftime('%Y-%m-%d')
            hora_actual = ahora.strftime('%H:%M:%S')
            
            # Crear objeto nota
            nota = NotaCreditoDebito(tipo_nota)
            
            # Obtener datos del formulario
            nota.datos['numero'] = getattr(self, f'numero_{tipo_nota}_var').get()
            nota.datos['fecha_emision'] = getattr(self, f'fecha_{tipo_nota}_var').get()
            nota.datos['factura_referencia'] = getattr(self, f'factura_ref_{tipo_nota}_var').get()
            nota.datos['codigo_concepto'] = getattr(self, f'codigo_concepto_{tipo_nota}_var').get()
            nota.datos['descripcion_concepto'] = getattr(self, f'descripcion_{tipo_nota}_text').get('1.0', tk.END).strip()
            nota.datos['valor_base'] = Decimal(getattr(self, f'valor_base_{tipo_nota}_var').get() or '0')
            nota.datos['porcentaje_iva'] = Decimal(getattr(self, f'iva_{tipo_nota}_var').get() or '0')
            nota.datos['valor_iva'] = Decimal(getattr(self, f'valor_iva_{tipo_nota}_var').get() or '0')
            nota.datos['valor_total'] = Decimal(getattr(self, f'total_{tipo_nota}_var').get() or '0')
            
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
             valor_iva, valor_total, cufe, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                nota.datos['numero'],
                tipo_nota,
                nota.datos['fecha_emision'],
                hora_actual,  # Usar la variable definida arriba
                nota.datos['factura_referencia'],
                nota.datos['codigo_concepto'],
                nota.datos['descripcion_concepto'],
                float(nota.datos['valor_base']),
                float(nota.datos['porcentaje_iva']),
                float(nota.datos['valor_iva']),
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
        getattr(self, f'iva_{tipo_nota}_var').set('19.00')
        getattr(self, f'valor_iva_{tipo_nota}_var').set('0.00')
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

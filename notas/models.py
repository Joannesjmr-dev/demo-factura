from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Factura(models.Model):
    """Modelo para facturas de referencia"""
    numero_documento = models.CharField(max_length=20, verbose_name="NIT Emisor")
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    numero_factura = models.CharField(max_length=50, unique=True, verbose_name="Número Factura")
    subtotal_factura = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Subtotal")
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="IVA")
    ic = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="IC")
    inc = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="INC")
    ica = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ICA")
    rete_fuente = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Retención Fuente")
    fecha_recepcion = models.DateField(verbose_name="Fecha Recepción")
    fecha_emision = models.DateField(verbose_name="Fecha Emisión")
    fecha_vencimiento = models.DateField(verbose_name="Fecha Vencimiento")
    total_retenciones = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Total Retenciones")
    total_factura = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Total Factura")
    tipo_cliente = models.CharField(max_length=50, verbose_name="Tipo Cliente")
    periodo_factura = models.CharField(max_length=50, verbose_name="Período Factura")
    notas_finales = models.TextField(blank=True, verbose_name="Notas Finales")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'facturas'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.razon_social}"

class NotaCreditoDebito(models.Model):
    """Modelo para notas crédito y débito DIAN"""
    TIPO_CHOICES = [
        ('credito', 'Nota Crédito'),
        ('debito', 'Nota Débito'),
    ]
    ESTADO_CHOICES = [
        ('generado', 'Generado'),
        ('enviado', 'Enviado'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Número Nota")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo Nota")
    tipo_operacion = models.CharField(max_length=10, verbose_name="Tipo Operación")
    fecha_emision = models.DateField(verbose_name="Fecha Emisión")
    hora_emision = models.TimeField(verbose_name="Hora Emisión")
    factura_referencia = models.CharField(max_length=50, verbose_name="Factura Referencia")
    codigo_concepto = models.CharField(max_length=10, verbose_name="Código Concepto")
    descripcion_concepto = models.TextField(verbose_name="Descripción Concepto")
    valor_base = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0'))], verbose_name="Valor Base")
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="% IVA")
    valor_iva = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor IVA")
    retencion_renta = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Retención Renta")
    porcentaje_retencion = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="% Retención")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Total")
    cufe = models.CharField(max_length=255, blank=True, verbose_name="CUFE")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='generado', verbose_name="Estado")
    nit_emisor = models.CharField(max_length=20, verbose_name="NIT Emisor")
    razon_social_emisor = models.CharField(max_length=255, verbose_name="Razón Social Emisor")
    valor_bruto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Bruto")
    total_bruto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Total Bruto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notas_credito_debito'
        verbose_name = 'Nota Crédito/Débito'
        verbose_name_plural = 'Notas Crédito/Débito'
        ordering = ['-fecha_emision', '-numero']

    def __str__(self):
        return f"{self.get_tipo_display()} {self.numero}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validaciones adicionales si es necesario
        pass

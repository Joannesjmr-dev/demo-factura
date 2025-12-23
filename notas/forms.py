from django import forms
from .models import NotaCreditoDebito
from .utils import ValidadorDIAN
from datetime import datetime

class NotaCreditoDebitoForm(forms.ModelForm):
    """Formulario para crear/editar notas crédito y débito"""

    TIPO_OPERACION_CHOICES_CREDITO = [
        ('20', '20 - Nota Crédito que referencia una factura electrónica'),
        ('22', '22 - Nota Crédito sin referencia a facturas'),
    ]

    TIPO_OPERACION_CHOICES_DEBITO = [
        ('30', '30 - Nota Débito que referencia una factura electrónica'),
        ('32', '32 - Nota Débito sin referencia a facturas'),
    ]

    CONCEPTO_CHOICES_CREDITO = [
        ('1', '1 - Devolución parcial de los bienes y/o no aceptación parcial del servicio'),
        ('2', '2 - Anulación de factura electrónica'),
        ('3', '3 - Rebaja o descuento parcial o total'),
        ('4', '4 - Ajuste de precio'),
        ('5', '5 - Descuento comercial por pronto pago'),
        ('6', '6 - Descuento comercial por volumen de ventas'),
        ('7', '7 - Otros'),
    ]

    CONCEPTO_CHOICES_DEBITO = [
        ('1', '1 - Intereses'),
        ('2', '2 - Gastos por cobrar'),
        ('3', '3 - Cambio del valor'),
        ('4', '4 - Otros'),
    ]

    tipo_operacion = forms.ChoiceField(choices=TIPO_OPERACION_CHOICES_CREDITO, required=True)
    codigo_concepto = forms.ChoiceField(choices=CONCEPTO_CHOICES_CREDITO, required=True)
    descripcion_concepto = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    fecha_emision = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.now().date())
    hora_emision = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), initial=datetime.now().time())

    class Meta:
        model = NotaCreditoDebito
        fields = [
            'numero', 'tipo', 'tipo_operacion', 'fecha_emision', 'hora_emision',
            'factura_referencia', 'codigo_concepto', 'descripcion_concepto',
            'valor_base', 'porcentaje_iva', 'valor_iva', 'retencion_renta',
            'porcentaje_retencion', 'valor_total', 'nit_emisor', 'razon_social_emisor',
            'valor_bruto', 'total_bruto'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'placeholder': 'Número de la nota'}),
            'factura_referencia': forms.TextInput(attrs={'placeholder': 'Número de factura referencia'}),
            'nit_emisor': forms.TextInput(attrs={'placeholder': 'NIT del emisor'}),
            'razon_social_emisor': forms.TextInput(attrs={'placeholder': 'Razón social del emisor'}),
            'valor_base': forms.NumberInput(attrs={'step': '0.01'}),
            'porcentaje_iva': forms.NumberInput(attrs={'step': '0.01'}),
            'valor_iva': forms.NumberInput(attrs={'readonly': True}),
            'retencion_renta': forms.NumberInput(attrs={'readonly': True}),
            'porcentaje_retencion': forms.NumberInput(attrs={'step': '0.01'}),
            'valor_total': forms.NumberInput(attrs={'readonly': True}),
            'valor_bruto': forms.NumberInput(attrs={'step': '0.01'}),
            'total_bruto': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo', 'credito')
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si es edición, ajustar choices según tipo
            if self.instance.tipo == 'credito':
                self.fields['tipo_operacion'].choices = self.TIPO_OPERACION_CHOICES_CREDITO
                self.fields['codigo_concepto'].choices = self.CONCEPTO_CHOICES_CREDITO
            else:
                self.fields['tipo_operacion'].choices = self.TIPO_OPERACION_CHOICES_DEBITO
                self.fields['codigo_concepto'].choices = self.CONCEPTO_CHOICES_DEBITO
        else:
            # Para nueva nota, ajustar choices según tipo pasado
            if tipo == 'credito':
                self.fields['tipo_operacion'].choices = self.TIPO_OPERACION_CHOICES_CREDITO
                self.fields['codigo_concepto'].choices = self.CONCEPTO_CHOICES_CREDITO
            else:
                self.fields['tipo_operacion'].choices = self.TIPO_OPERACION_CHOICES_DEBITO
                self.fields['codigo_concepto'].choices = self.CONCEPTO_CHOICES_DEBITO
            # Setear initial para tipo
            self.fields['tipo'].initial = tipo

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        # Verificar que no exista
        if NotaCreditoDebito.objects.filter(numero=numero).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError('El número de nota ya existe.')
        return numero

    def clean_nit_emisor(self):
        nit = self.cleaned_data.get('nit_emisor')
        if nit and not ValidadorDIAN.validar_nit(nit):
            raise forms.ValidationError('NIT inválido.')
        return nit

    def clean_codigo_concepto(self):
        codigo = self.cleaned_data.get('codigo_concepto')
        tipo = self.cleaned_data.get('tipo')
        if tipo == 'credito' and not ValidadorDIAN.validar_concepto_nota_credito(codigo):
            raise forms.ValidationError('Código de concepto inválido para nota crédito.')
        elif tipo == 'debito' and not ValidadorDIAN.validar_concepto_nota_debito(codigo):
            raise forms.ValidationError('Código de concepto inválido para nota débito.')
        return codigo

class ConsultaNotasForm(forms.Form):
    """Formulario para consultas de notas"""
    tipo = forms.ChoiceField(
        choices=[('', 'Todos'), ('credito', 'Nota Crédito'), ('debito', 'Nota Débito')],
        required=False,
        initial=''
    )
    fecha_desde = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.now().date().replace(day=1)
    )
    fecha_hasta = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.now().date()
    )

class ReporteNotasForm(forms.Form):
    """Formulario para reportes Excel"""
    tipo = forms.ChoiceField(
        choices=[('', 'Todos'), ('credito', 'Nota Crédito'), ('debito', 'Nota Débito')],
        required=False,
        initial=''
    )
    fecha_desde = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.now().date().replace(day=1)
    )
    fecha_hasta = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.now().date()
    )
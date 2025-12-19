from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
import pandas as pd
import os
from datetime import datetime
from .models import NotaCreditoDebito, Factura
from .forms import NotaCreditoDebitoForm, ConsultaNotasForm, ReporteNotasForm
from .utils import GeneradorXML

class IndexView(View):
    """Vista principal - redirige a la lista de notas"""
    def get(self, request):
        return redirect('notas:consulta')

class NotaCreateView(SuccessMessageMixin, CreateView):
    """Vista para crear nueva nota"""
    model = NotaCreditoDebito
    form_class = NotaCreditoDebitoForm
    template_name = 'notas/nota_form.html'
    success_url = '/notas/consulta/'
    success_message = "Nota generada con éxito"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tipo'] = self.request.GET.get('tipo', 'credito')
        return kwargs

    def form_valid(self, form):
        # Calcular valores automáticos
        form.instance.valor_iva = (form.instance.valor_base * form.instance.porcentaje_iva) / 100
        form.instance.retencion_renta = (form.instance.valor_bruto * form.instance.porcentaje_retencion) / 100
        form.instance.valor_total = form.instance.valor_bruto + form.instance.valor_iva - form.instance.retencion_renta
        return super().form_valid(form)

class NotaUpdateView(SuccessMessageMixin, UpdateView):
    """Vista para editar nota"""
    model = NotaCreditoDebito
    form_class = NotaCreditoDebitoForm
    template_name = 'notas/nota_form.html'
    success_url = '/notas/consulta/'
    success_message = "Nota actualizada con éxito"

    def form_valid(self, form):
        # Recalcular valores
        form.instance.valor_iva = (form.instance.valor_base * form.instance.porcentaje_iva) / 100
        form.instance.retencion_renta = (form.instance.valor_bruto * form.instance.porcentaje_retencion) / 100
        form.instance.valor_total = form.instance.valor_bruto + form.instance.valor_iva - form.instance.retencion_renta
        return super().form_valid(form)

class ConsultaNotasView(ListView):
    """Vista para consultar notas"""
    model = NotaCreditoDebito
    template_name = 'notas/consulta.html'
    context_object_name = 'notas'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ConsultaNotasForm(self.request.GET)
        if form.is_valid():
            tipo = form.cleaned_data.get('tipo')
            fecha_desde = form.cleaned_data.get('fecha_desde')
            fecha_hasta = form.cleaned_data.get('fecha_hasta')

            if tipo:
                queryset = queryset.filter(tipo=tipo)
            if fecha_desde and fecha_hasta:
                queryset = queryset.filter(fecha_emision__range=[fecha_desde, fecha_hasta])

        return queryset.order_by('-fecha_emision', '-numero')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ConsultaNotasForm(self.request.GET or None)
        return context

class ReporteNotasView(View):
    """Vista para generar reportes Excel"""

    def get(self, request):
        form = ReporteNotasForm(request.GET or None)
        if form.is_valid():
            tipo = form.cleaned_data.get('tipo')
            fecha_desde = form.cleaned_data.get('fecha_desde')
            fecha_hasta = form.cleaned_data.get('fecha_hasta')

            queryset = NotaCreditoDebito.objects.all()
            if tipo:
                queryset = queryset.filter(tipo=tipo)
            if fecha_desde and fecha_hasta:
                queryset = queryset.filter(fecha_emision__range=[fecha_desde, fecha_hasta])

            queryset = queryset.order_by('-fecha_emision', '-numero')

            if queryset.exists():
                # Crear DataFrame
                data = []
                for nota in queryset:
                    data.append({
                        'Número': nota.numero,
                        'Tipo': nota.get_tipo_display(),
                        'Tipo Operación': nota.tipo_operacion,
                        'Fecha Emisión': nota.fecha_emision,
                        'Factura Referencia': nota.factura_referencia,
                        'Código Concepto': nota.codigo_concepto,
                        'Descripción Concepto': nota.descripcion_concepto,
                        'Valor Base': float(nota.valor_base),
                        '% IVA': float(nota.porcentaje_iva),
                        'Valor IVA': float(nota.valor_iva),
                        '% Retención': float(nota.porcentaje_retencion),
                        'Retención Renta': float(nota.retencion_renta),
                        'Valor Total': float(nota.valor_total),
                        'Estado': nota.get_estado_display(),
                        'NIT Emisor': nota.nit_emisor,
                        'Razón Social Emisor': nota.razon_social_emisor,
                        'Total Bruto': float(nota.total_bruto),
                    })

                df = pd.DataFrame(data)

                # Crear directorio si no existe
                os.makedirs('reportes', exist_ok=True)
                nombre_archivo = f"reportes/reporte_notas_{fecha_desde}_a_{fecha_hasta}.xlsx"
                df.to_excel(nombre_archivo, index=False)

                messages.success(request, f"Reporte exportado exitosamente a: {nombre_archivo}")
            else:
                messages.warning(request, "No hay datos para exportar en el rango seleccionado.")

        return render(request, 'notas/reportes.html', {'form': form})

def buscar_factura(request):
    """Vista AJAX para buscar factura por número"""
    numero = request.GET.get('numero', '').strip()
    if numero:
        try:
            factura = Factura.objects.get(numero_factura=numero)
            data = {
                'success': True,
                'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d'),
                'nit_emisor': factura.numero_documento,
                'razon_social': factura.razon_social,
                'total_bruto': str(factura.total_factura),
                'valor_bruto': str(factura.subtotal_factura),
            }
        except Factura.DoesNotExist:
            data = {'success': False, 'message': 'Factura no encontrada'}
    else:
        data = {'success': False, 'message': 'Número de factura requerido'}

    from django.http import JsonResponse
    return JsonResponse(data)

def exportar_xml(request, pk):
    """Vista para exportar XML de una nota"""
    nota = get_object_or_404(NotaCreditoDebito, pk=pk)
    generador = GeneradorXML(nota)
    xml_content = generador.generar_xml()

    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="nota_{nota.numero}.xml"'
    return response

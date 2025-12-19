from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('crear/', views.NotaCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', views.NotaUpdateView.as_view(), name='editar'),
    path('consulta/', views.ConsultaNotasView.as_view(), name='consulta'),
    path('reportes/', views.ReporteNotasView.as_view(), name='reportes'),
    path('buscar_factura/', views.buscar_factura, name='buscar_factura'),
    path('exportar_xml/<int:pk>/', views.exportar_xml, name='exportar_xml'),
]
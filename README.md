# Módulo Notas Crédito y Débito - DIAN

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-6.0-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Este proyecto es una aplicación web desarrollada en Django que permite generar, gestionar y consultar notas crédito y débito electrónicas conforme a la normativa de la Dirección de Impuestos y Aduanas Nacionales (DIAN) de Colombia, según el Anexo Técnico 1.9.

## 🚀 Características Principales

- ✅ Generación de Notas Crédito y Débito electrónicas
- ✅ Validación automática de datos según normas DIAN
- ✅ Consulta y filtrado avanzado de notas
- ✅ Generación de reportes Excel
- ✅ Exportación XML compatible con DIAN
- ✅ Interfaz web moderna con Bootstrap
- ✅ Base de datos SQLite/MySQL
- ✅ API REST para integraciones

## 📋 Requisitos del Sistema

- **Python**: 3.12 o superior
- **Gestor de dependencias**: uv (recomendado) o pip
- **Base de datos**: SQLite (desarrollo) / MySQL (producción)
- **Navegador web**: Chrome, Firefox, Safari, Edge (versión reciente)

## 🛠️ Instalación

### Opción 1: Usando uv (Recomendado)

```bash
# Crear entorno virtual
uv venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate

# Instalar dependencias
uv pip install -r requirements.txt
```

### Opción 2: Usando pip

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## ⚙️ Configuración

### Base de Datos

Por defecto, la aplicación usa SQLite. Para usar MySQL en producción:

1. Instalar MySQL Server
2. Crear base de datos:
```sql
CREATE DATABASE facturacion_dian CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
3. Actualizar `notas_dian/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'facturacion_dian',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Migraciones

```bash
# Ejecutar migraciones
python manage.py migrate
```

## 🚀 Ejecución

### Modo Desarrollo

```bash
# Ejecutar servidor de desarrollo
python main.py
# O directamente con Django:
# python manage.py runserver
```

La aplicación estará disponible en: http://localhost:8000

### Modo Producción

Para despliegue en producción, usar un servidor WSGI como Gunicorn:

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn notas_dian.wsgi:application --bind 0.0.0.0:8000
```

## 📖 Uso

### Crear una Nota

1. Acceder a la aplicación web
2. Hacer clic en "Nueva Nota Crédito" o "Nueva Nota Débito"
3. Completar el formulario con los datos requeridos
4. El sistema calculará automáticamente los valores
5. Guardar la nota

### Consultar Notas

- Usar el menú "Consultas" para filtrar por tipo, fechas, etc.
- Los resultados se muestran en una tabla paginada

### Generar Reportes

- Ir a "Reportes" y seleccionar rango de fechas
- El sistema genera un archivo Excel automáticamente

### Exportar XML

- Desde la consulta, hacer clic en el botón de exportar XML
- El archivo se descarga automáticamente

## 🏗️ Arquitectura

La aplicación sigue una arquitectura MVC (Model-View-Controller) con:

- **Modelos**: Definición de datos (Factura, NotaCreditoDebito)
- **Vistas**: Lógica de negocio y presentación
- **Templates**: Interfaz de usuario HTML
- **URLs**: Enrutamiento de peticiones

Para más detalles, ver [`docs/arquitectura.md`](docs/arquitectura.md).

## 📊 Modelos de Datos

### Factura
- Referencias de facturas para notas
- Campos: NIT emisor, razón social, número factura, valores, fechas

### NotaCreditoDebito
- Notas electrónicas DIAN
- Tipos: Crédito, Débito
- Estados: Generado, Enviado, Aceptado, Rechazado

## 🔧 Desarrollo

### Estructura del Proyecto

```
notas_dian/
├── notas_dian/          # Configuración Django
├── notas/              # App principal
├── templates/          # Plantillas HTML
├── static/             # CSS, JS, imágenes
├── databases/          # Scripts SQL
├── reportes/           # Reportes generados
└── docs/               # Documentación
```

### Comandos Útiles

```bash
# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic
```

## 📚 Documentación

- [Arquitectura del Sistema](docs/arquitectura.md)
- [Guía de Instalación](docs/instalacion.md)
- [Guía del Usuario](docs/usuario.md)
- [Documentación de API](docs/api.md)
- [Guía de Desarrollo](docs/desarrollo.md)

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o reportar bugs:

- Crear un issue en GitHub
- Revisar la documentación en `docs/`
- Contactar al equipo de desarrollo

## 🔄 Versiones

### v0.1.0
- ✅ Funcionalidad básica de notas crédito/débito
- ✅ Interfaz web con Bootstrap
- ✅ Generación de reportes Excel
- ✅ Exportación XML DIAN
- ✅ Base de datos SQLite/MySQL

### Próximas versiones
- 🔄 Integración completa con DIAN
- 🔄 Generación de PDF
- 🔄 API REST completa
- 🔄 Dashboard administrativo avanzado

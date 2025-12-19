# Guía de Desarrollo - Módulo Notas Crédito y Débito DIAN

Esta guía proporciona información técnica para desarrolladores que trabajan en el proyecto, incluyendo configuración del entorno, estructura del código, mejores prácticas y procesos de desarrollo.

## 🛠️ Configuración del Entorno de Desarrollo

### Prerrequisitos

```bash
# Python 3.12+
python --version

# Git
git --version

# uv (recomendado)
pip install uv
```

### Clonación y Configuración Inicial

```bash
# Clonar repositorio
git clone https://github.com/tu-organizacion/notas-dian.git
cd notas-dian

# Configurar entorno virtual con uv
uv venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
uv pip install -r requirements.txt

# Configurar pre-commit hooks (si existen)
pre-commit install
```

### Variables de Entorno

Crear archivo `.env` para configuración local:

```bash
# .env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///db.sqlite3
DJANGO_SETTINGS_MODULE=notas_dian.settings
```

## 🏗️ Estructura del Proyecto

```
notas_dian/
├── .venv/                      # Entorno virtual
├── notas_dian/                 # Configuración Django
│   ├── __init__.py
│   ├── settings.py            # Configuración principal
│   ├── urls.py                # URLs raíz
│   ├── wsgi.py                # WSGI para producción
│   └── asgi.py                # ASGI (futuro)
├── notas/                     # App principal
│   ├── migrations/            # Migraciones DB
│   ├── __init__.py
│   ├── admin.py               # Admin Django
│   ├── apps.py                # Configuración app
│   ├── forms.py               # Formularios Django
│   ├── models.py              # Modelos de datos
│   ├── tests.py               # Tests unitarios
│   ├── urls.py                # URLs de la app
│   ├── utils.py               # Utilidades
│   └── views.py               # Vistas
├── templates/                 # Plantillas HTML
│   ├── base.html              # Base común
│   └── notas/                 # Templates específicos
├── static/                    # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── scripts.js
├── databases/                 # Scripts SQL
├── reportes/                  # Reportes generados
├── docs/                      # Documentación
├── main.py                    # Script de ejecución
├── manage.py                  # Django management
├── pyproject.toml             # Configuración proyecto
├── requirements.txt           # Dependencias
├── uv.lock                    # Lock file uv
├── .gitignore                 # Git ignore
├── .python-version            # Versión Python
└── README.md                  # Documentación principal
```

## 🚀 Comandos de Desarrollo

### Servidor de Desarrollo

```bash
# Ejecutar servidor
python main.py
# o
python manage.py runserver

# Con puerto específico
python manage.py runserver 0.0.0.0:8000

# Con autoreload mejorado
python manage.py runserver --noreload
```

### Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Ver SQL de migración
python manage.py sqlmigrate notas 0001
```

### Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app
python manage.py test notas

# Con cobertura
coverage run manage.py test
coverage report

# Tests con verbose
python manage.py test --verbosity=2
```

### Archivos Estáticos

```bash
# Recopilar estáticos
python manage.py collectstatic

# Comprimir estáticos (si usa django-compressor)
python manage.py compress
```

### Internacionalización

```bash
# Crear archivos de traducción
python manage.py makemessages -l es

# Compilar traducciones
python manage.py compilemessages
```

## 📝 Desarrollo de Funcionalidades

### Agregar Nuevos Campos a Modelos

1. **Modificar modelo** en `notas/models.py`:
```python
class NotaCreditoDebito(models.Model):
    # ... campos existentes ...
    nuevo_campo = models.CharField(max_length=100, blank=True)
```

2. **Crear migración**:
```bash
python manage.py makemigrations notas
```

3. **Aplicar migración**:
```bash
python manage.py migrate
```

4. **Actualizar formulario** en `notas/forms.py`:
```python
class NotaCreditoDebitoForm(forms.ModelForm):
    class Meta:
        model = NotaCreditoDebito
        fields = ['numero', 'tipo', 'nuevo_campo', ...]
```

5. **Actualizar template** en `templates/notas/nota_form.html`

### Crear Nueva Vista

1. **Agregar vista** en `notas/views.py`:
```python
class NuevaVista(ListView):
    model = NotaCreditoDebito
    template_name = 'notas/nueva_vista.html'
    context_object_name = 'notas'
```

2. **Agregar URL** en `notas/urls.py`:
```python
urlpatterns = [
    # ... urls existentes ...
    path('nueva-vista/', NuevaVista.as_view(), name='nueva_vista'),
]
```

3. **Crear template** en `templates/notas/nueva_vista.html`

### Agregar Validaciones Personalizadas

En `notas/models.py`:
```python
class NotaCreditoDebito(models.Model):
    # ... campos ...

    def clean(self):
        if self.valor_base < 0:
            raise ValidationError('El valor base no puede ser negativo')
        if self.tipo == 'credito' and self.valor_total > 0:
            raise ValidationError('Nota crédito debe tener valor negativo')
```

### Implementar Cálculos Automáticos

En `notas/views.py`:
```python
class NotaCreateView(CreateView):
    # ... configuración ...

    def form_valid(self, form):
        # Cálculos automáticos
        form.instance.valor_iva = (form.instance.valor_base * form.instance.porcentaje_iva) / 100
        form.instance.retencion_renta = (form.instance.valor_bruto * form.instance.porcentaje_retencion) / 100
        form.instance.valor_total = form.instance.valor_bruto + form.instance.valor_iva - form.instance.retencion_renta
        return super().form_valid(form)
```

## 🧪 Testing

### Estructura de Tests

```python
# notas/tests.py
from django.test import TestCase
from .models import NotaCreditoDebito

class NotaCreditoDebitoTest(TestCase):
    def setUp(self):
        self.nota = NotaCreditoDebito.objects.create(
            numero='TEST001',
            tipo='credito',
            # ... otros campos
        )

    def test_calculo_valor_total(self):
        self.assertEqual(self.nota.valor_total, 100000)

    def test_str_representation(self):
        self.assertEqual(str(self.nota), 'Nota Crédito TEST001')
```

### Ejecutar Tests

```bash
# Tests específicos
python manage.py test notas.tests.NotaCreditoDebitoTest.test_calculo_valor_total

# Con coverage
pip install coverage
coverage run manage.py test
coverage html  # Genera reporte HTML
```

### Tipos de Tests

- **Unit Tests**: Probar funciones individuales
- **Integration Tests**: Probar interacción entre componentes
- **Functional Tests**: Probar flujos completos de usuario
- **Performance Tests**: Medir rendimiento

## 🔧 Debugging

### Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

Agregar a `settings.py`:
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### Logging

Configurar logging en `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### Breakpoints en VS Code

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver"],
            "django": true
        }
    ]
}
```

## 🚀 Despliegue

### Configuración de Producción

```python
# settings.py para producción
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Base de datos PostgreSQL/MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'notas_dian',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "notas_dian.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    volumes:
      - static:/app/static
  nginx:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static:/app/static
volumes:
  static:
```

## 📋 Mejores Prácticas

### Código

- **PEP 8**: Seguir estándares de Python
- **DRY**: No repetir código
- **SOLID**: Principios de diseño orientado a objetos
- **Documentación**: Docstrings en funciones y clases

### Git

```bash
# Flujo de trabajo
git checkout -b feature/nueva-funcionalidad
# ... desarrollo ...
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
# Crear PR
```

### Seguridad

- **SECRET_KEY**: Nunca commitear en código
- **DEBUG**: False en producción
- **ALLOWED_HOSTS**: Configurar explícitamente
- **HTTPS**: Siempre en producción
- **Dependencias**: Mantener actualizadas

### Rendimiento

- **Select Related/Prefetch**: Optimizar queries
- **Paginación**: Para listados grandes
- **Cache**: Implementar donde sea necesario
- **CDN**: Para archivos estáticos

## 🔄 CI/CD

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: python manage.py test
```

## 📚 Recursos Adicionales

### Documentación Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/) (para APIs futuras)

### Herramientas Recomendadas
- **Black**: Formateo de código
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pre-commit**: Hooks de pre-commit

### Comunidad
- [Django Forum](https://forum.djangoproject.com/)
- [Django Discord](https://discord.gg/django)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/django)

## 🤝 Contribución

### Proceso
1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Estándares de Código
- Usar Black para formateo
- Escribir tests para nuevas funcionalidades
- Actualizar documentación
- Seguir convenciones de commits

Esta guía proporciona las bases para desarrollar eficientemente en el proyecto. Para preguntas específicas, consultar la documentación de Django o contactar al equipo de desarrollo.
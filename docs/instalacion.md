# Guía de Instalación - Módulo Notas Crédito y Débito DIAN

Esta guía proporciona instrucciones detalladas para instalar y configurar el Módulo Notas Crédito y Débito DIAN en diferentes entornos.

## 📋 Prerrequisitos

### Requisitos Mínimos del Sistema

- **Sistema Operativo**: Windows 10+, macOS 10.15+, Ubuntu 18.04+ o equivalente
- **Procesador**: 1 GHz o superior
- **Memoria RAM**: 2 GB mínimo, 4 GB recomendado
- **Espacio en disco**: 500 MB para instalación + espacio para datos
- **Conexión a internet**: Para descarga de dependencias

### Software Requerido

- **Python 3.12** o superior
- **Gestor de dependencias**: uv (recomendado) o pip
- **Git**: Para clonar el repositorio (opcional)

### Verificación de Prerrequisitos

```bash
# Verificar versión de Python
python --version
# Debe mostrar Python 3.12.x o superior

# Verificar pip
pip --version

# Verificar uv (opcional pero recomendado)
uv --version
```

## 🚀 Instalación Paso a Paso

### Paso 1: Obtener el Código Fuente

#### Opción A: Clonar desde Git (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/tu-organizacion/notas-dian.git
cd notas-dian
```

#### Opción B: Descargar ZIP

1. Descargar el archivo ZIP desde GitHub
2. Extraer el contenido en una carpeta local
3. Abrir terminal en la carpeta del proyecto

### Paso 2: Configurar Entorno Virtual

#### Usando uv (Recomendado)

```bash
# Crear entorno virtual
uv venv .venv

# Activar entorno virtual
# En Windows (PowerShell):
.venv\Scripts\activate
# En Windows (Command Prompt):
.venv\Scripts\activate.bat
# En Linux/Mac:
source .venv/bin/activate
```

#### Usando venv (Python estándar)

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Instalar dependencias del proyecto
uv pip install -r requirements.txt

# O usando pip:
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos

#### Opción A: SQLite (Desarrollo - Recomendado)

No requiere configuración adicional. SQLite se crea automáticamente.

#### Opción B: MySQL (Producción)

```bash
# Instalar MySQL Server (Ubuntu/Debian)
sudo apt update
sudo apt install mysql-server

# Instalar MySQL Server (Windows)
# Descargar e instalar desde https://dev.mysql.com/downloads/mysql/

# Instalar MySQL Server (macOS)
brew install mysql

# Crear base de datos
mysql -u root -p
```

```sql
-- Ejecutar en MySQL
CREATE DATABASE facturacion_dian
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Crear usuario (opcional)
CREATE USER 'notas_user'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON facturacion_dian.* TO 'notas_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 5: Configurar la Aplicación

#### Archivo de Configuración

Editar `notas_dian/settings.py` según sea necesario:

```python
# Para MySQL (descomentar y configurar si es necesario)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'facturacion_dian',
#         'USER': 'notas_user',
#         'PASSWORD': 'password_seguro',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#         }
#     }
# }

# Configuración de zona horaria (opcional)
TIME_ZONE = 'America/Bogota'

# Configuración de idioma (opcional)
LANGUAGE_CODE = 'es-co'
```

#### Variables de Entorno (Opcional)

Crear archivo `.env` en la raíz del proyecto:

```bash
# .env
DEBUG=True
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DATABASE_URL=mysql://user:password@localhost/facturacion_dian
```

### Paso 6: Ejecutar Migraciones

```bash
# Aplicar migraciones de base de datos
python manage.py migrate

# Crear superusuario (opcional, para acceder al admin)
python manage.py createsuperuser
```

### Paso 7: Verificar Instalación

```bash
# Ejecutar servidor de desarrollo
python main.py

# O directamente:
python manage.py runserver
```

Abrir navegador en `http://localhost:8000` y verificar que la aplicación carga correctamente.

## 🔧 Configuración Avanzada

### Configuración de Email (Opcional)

Para envío de notificaciones por email, configurar en `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-app-password'
```

### Configuración de Archivos Estáticos

```bash
# Recopilar archivos estáticos para producción
python manage.py collectstatic
```

### Configuración de Logging

Editar `settings.py` para configurar logs:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🚀 Despliegue en Producción

### Usando Gunicorn + Nginx

#### Instalar Gunicorn

```bash
pip install gunicorn
```

#### Configurar Nginx

Crear archivo `/etc/nginx/sites-available/notas_dian`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /ruta/a/tu/proyecto/static/;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

#### Crear Servicio Systemd

Crear archivo `/etc/systemd/system/notas-dian.service`:

```ini
[Unit]
Description=Notas DIAN Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/ruta/a/tu/proyecto
Environment="PATH=/ruta/a/tu/proyecto/.venv/bin"
ExecStart=/ruta/a/tu/proyecto/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 notas_dian.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Iniciar Servicios

```bash
# Habilitar sitio Nginx
sudo ln -s /etc/nginx/sites-available/notas_dian /etc/nginx/sites-enabled/

# Iniciar servicios
sudo systemctl start notas-dian
sudo systemctl enable notas-dian
sudo systemctl restart nginx
```

### Usando Docker

#### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "notas_dian.wsgi:application"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - ./static:/app/static
    environment:
      - DEBUG=False
      - SECRET_KEY=tu-clave-secreta
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: facturacion_dian
      MYSQL_USER: notas_user
      MYSQL_PASSWORD: password_seguro
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 🔍 Solución de Problemas

### Error: "Python version not supported"

**Solución**: Actualizar Python a versión 3.12 o superior.

### Error: "Module not found"

**Solución**: Asegurarse de que el entorno virtual esté activado y las dependencias instaladas.

```bash
# Verificar entorno virtual
which python
# Debe apuntar a .venv/bin/python

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "Database connection failed"

**Solución**: Verificar configuración de base de datos en `settings.py`.

### Error: "Permission denied"

**Solución**: Ajustar permisos de archivos.

```bash
# Dar permisos de ejecución
chmod +x main.py

# Cambiar propietario (Linux/Mac)
sudo chown -R $USER:$USER /ruta/al/proyecto
```

### Error: "Port already in use"

**Solución**: Cambiar puerto o matar proceso existente.

```bash
# Ver procesos en puerto 8000
lsof -i :8000

# Matar proceso
kill -9 <PID>
```

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. Verificar los logs de error
2. Consultar la documentación completa
3. Revisar issues en GitHub
4. Contactar al equipo de soporte

## ✅ Verificación Final

Después de la instalación, verificar:

- ✅ La aplicación carga en el navegador
- ✅ Se pueden crear notas sin errores
- ✅ Los reportes se generan correctamente
- ✅ La base de datos guarda los datos
- ✅ No hay errores en la consola del navegador

¡La instalación ha sido completada exitosamente!
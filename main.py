"""
Script principal para ejecutar el servidor Django de Notas DIAN
"""
import os
import sys

def main():
    """Ejecuta el servidor Django"""
    # Agregar el directorio actual al path de Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)

    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notas_dian.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado?"
        ) from exc

    # Ejecutar runserver por defecto
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main()

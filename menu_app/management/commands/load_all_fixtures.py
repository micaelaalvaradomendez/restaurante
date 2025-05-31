from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os
import glob
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Carga todos los fixtures existentes en el proyecto'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Resetea la base de datos antes de cargar los fixtures (elimina todas las tablas)',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Reseteando la base de datos...'))
            call_command('flush', '--noinput')
            self.stdout.write(self.style.SUCCESS('Base de datos reseteada.'))

        self.stdout.write(self.style.NOTICE('Buscando fixtures en todas las aplicaciones...'))
        
        # Obtener todas las aplicaciones instaladas
        app_configs = settings.INSTALLED_APPS
        
        # Lista para almacenar los paths de los fixtures encontrados
        fixtures_paths = []
        
        # Buscar fixtures en cada aplicación
        for app in app_configs:
            if '.' not in app:  # Ignorar apps del sistema como django.contrib.*
                try:
                    app_path = os.path.join(settings.BASE_DIR, app, 'fixtures')
                    if os.path.exists(app_path):
                        fixture_files = glob.glob(os.path.join(app_path, '*.json'))
                        for fixture_file in fixture_files:
                            fixtures_paths.append(os.path.relpath(fixture_file, settings.BASE_DIR))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al buscar fixtures en {app}: {str(e)}'))
        
        if not fixtures_paths:
            self.stdout.write(self.style.WARNING('No se encontraron fixtures para cargar.'))
            return
        
        # Ordenar los fixtures para cargar primero los modelos básicos
        # Este orden es importante para mantener la integridad referencial
        priority_order = ['users', 'category', 'product', 'rating']
        
        def get_fixture_priority(fixture_path):
            for i, name in enumerate(priority_order):
                if name in fixture_path:
                    return i
            return len(priority_order)
        
        fixtures_paths.sort(key=get_fixture_priority)
        
        # Mostrar los fixtures encontrados
        self.stdout.write(self.style.SUCCESS(f'Se encontraron {len(fixtures_paths)} fixtures:'))
        for i, path in enumerate(fixtures_paths, 1):
            self.stdout.write(f'  {i}. {path}')
        
        # Cargar cada fixture en orden
        self.stdout.write(self.style.NOTICE('Cargando fixtures...'))
        success_count = 0
        error_count = 0
        
        for fixture_path in fixtures_paths:
            try:
                self.stdout.write(f'Cargando {fixture_path}...')
                result = call_command('loaddata', fixture_path, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f'  ✓ {fixture_path} cargado exitosamente.'))
                success_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error al cargar {fixture_path}: {str(e)}'))
                error_count += 1
        
        # Mostrar resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Proceso completado: {success_count} fixtures cargados exitosamente, {error_count} errores.'))

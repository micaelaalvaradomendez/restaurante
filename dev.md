# Bitácora de Desarrollo - Restaurante

## Historial de Desarrollo

### 30 de mayo de 2025
- Reorganización de modelos: Separación de modelos en archivos individuales dentro de un módulo
- Reorganización de vistas: Separación de vistas en archivos individuales dentro de un módulo
- Creación de fixtures para categorías, productos y calificaciones
- Configuración correcta del modelo de usuario personalizado
- Creación del comando personalizado `load_all_fixtures` para facilitar la carga de datos iniciales

## Estructura del Proyecto

El proyecto sigue una estructura modular:

```
restaurante/
├── menu_app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── rating.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── home_view.py
│   │   ├── menu_list_view.py
│   │   └── product_detail_view.py
│   ├── fixtures/
│   │   ├── categories.json
│   │   ├── products.json
│   │   └── ratings.json
│   └── ...
└── ...
```

## Buenas Prácticas

### Buenas Prácticas de Django

1. **Estructura de Aplicaciones**
   - Mantener aplicaciones pequeñas y enfocadas en una única funcionalidad
   - Organizar modelos y vistas en módulos separados cuando crezcan
   - Seguir el principio DRY (Don't Repeat Yourself)

2. **Modelos**
   - Definir métodos `__str__` para todos los modelos
   - Usar modelos de relación correctos (`ForeignKey`, `ManyToManyField`, etc.)
   - Implementar métodos para operaciones comunes en los modelos
   - Usar `related_name` en relaciones para evitar conflictos

3. **Vistas**
   - Preferir vistas basadas en clases sobre vistas basadas en funciones
   - Usar mixins para reutilizar funcionalidad
   - Mantener la lógica de negocio fuera de las vistas
   - Seguir el patrón de nombramiento: `model_action.html` (ej. `product_detail.html`)

4. **Formularios**
   - Usar `ModelForm` cuando sea posible
   - Definir validaciones en el modelo y no en la vista
   - Personalizar mensajes de error de validación

5. **Plantillas**
   - Usar herencia de plantillas para mantener un diseño consistente
   - Crear bloques para secciones reutilizables
   - No incluir lógica compleja en las plantillas

6. **Admin**
   - Personalizar la interfaz de administración para facilitar la gestión
   - Usar `list_display`, `search_fields` y `list_filter`
   - Implementar acciones personalizadas para operaciones por lotes

7. **Seguridad**
   - No exponer información sensible en URLs o plantillas
   - Validar entrada de usuario tanto en el cliente como en el servidor
   - Usar HTTPS en producción
   - Proteger contra ataques CSRF, XSS, SQL Injection, etc.

8. **Rendimiento**
   - Usar `select_related()` y `prefetch_related()` para optimizar consultas
   - Implementar paginación para conjuntos de datos grandes
   - Cachear resultados de consultas frecuentes
   - Usar consultas complejas en lugar de múltiples consultas simples

9. **Pruebas**
   - Escribir pruebas unitarias, de integración y funcionales
   - Usar fixtures para datos de prueba
   - Implementar CI/CD para ejecutar pruebas automáticamente

10. **Despliegue**
    - Usar archivos de configuración específicos para cada entorno
    - No almacenar secretos en el código
    - Usar variables de entorno para configuración sensible
    - Implementar logging para facilitar la depuración

### Buenas Prácticas de Python

1. **Estilo de Código**
   - Seguir PEP 8 para convenciones de estilo
   - Usar un linter (flake8, ruff) para verificar el cumplimiento
   - Mantener longitud de línea a 79-88 caracteres
   - Usar nombres de variables descriptivos

2. **Documentación**
   - Documentar todas las funciones, clases y métodos con docstrings
   - Mantener un README actualizado
   - Incluir ejemplos de uso en la documentación

3. **Gestión de Dependencias**
   - Usar entornos virtuales para aislar dependencias
   - Mantener un archivo `requirements.txt` actualizado
   - Especificar versiones exactas de dependencias

4. **Organización del Código**
   - Dividir código en módulos lógicos
   - Evitar archivos grandes con demasiadas responsabilidades
   - Seguir principios SOLID

5. **Manejo de Errores**
   - Usar try/except de manera específica
   - Crear excepciones personalizadas cuando sea necesario
   - Proporcionar mensajes de error útiles

6. **Control de Versiones**
   - Usar commits pequeños y específicos
   - Escribir mensajes de commit descriptivos
   - Utilizar ramas para nuevas características y correcciones

7. **Testing**
   - Escribir tests para todas las funcionalidades
   - Usar pytest para tests
   - Mantener alta cobertura de código (>80%)

## Comandos Útiles

### Manejo de Fixtures

```bash
# Crear fixtures a partir de datos existentes
python manage.py dumpdata menu_app.Category --indent 2 > menu_app/fixtures/categories.json

# Cargar fixtures individualmente
python manage.py loaddata menu_app/fixtures/categories.json

# Cargar todos los fixtures existentes automáticamente
python manage.py load_all_fixtures

# Cargar todos los fixtures con reseteo de base de datos
python manage.py load_all_fixtures --reset
```

### Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations
```

### Pruebas

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas de una aplicación específica
python manage.py test menu_app
```

### Shell

```bash
# Iniciar shell de Django
python manage.py shell

# Iniciar shell con soporte para IPython (requiere django-extensions)
python manage.py shell_plus
```

## Recursos Útiles

- [Documentación oficial de Django](https://docs.djangoproject.com/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/en/latest/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [TestDriven.io Django Tutorials](https://testdriven.io/blog/topics/django/)

## Comandos Personalizados

### load_all_fixtures

Este comando personalizado carga automáticamente todos los fixtures disponibles en el proyecto en un orden que respeta las dependencias entre modelos.

**Ubicación:** `menu_app/management/commands/load_all_fixtures.py`

**Uso básico:**
```bash
python manage.py load_all_fixtures
```

**Opciones:**
- `--reset`: Limpia la base de datos antes de cargar los fixtures (ejecuta `flush`)
```bash
python manage.py load_all_fixtures --reset
```

**Características:**
- Busca automáticamente todos los archivos JSON en las carpetas `fixtures` de todas las aplicaciones instaladas
- Ordena los fixtures para cargar primero los modelos base (users, category, product, rating)
- Muestra una lista de los fixtures encontrados antes de cargarlos
- Proporciona un resumen al final con la cantidad de fixtures cargados exitosamente y errores
- Maneja errores para que si un fixture falla, continúe con los demás

**Ejemplo de salida:**
```
Buscando fixtures en todas las aplicaciones...
Se encontraron 4 fixtures:
  1. users/fixtures/users.json
  2. menu_app/fixtures/categories.json
  3. menu_app/fixtures/products.json
  4. menu_app/fixtures/ratings.json
Cargando fixtures...
Cargando users/fixtures/users.json...
  ✓ users/fixtures/users.json cargado exitosamente.
Cargando menu_app/fixtures/categories.json...
  ✓ menu_app/fixtures/categories.json cargado exitosamente.
Cargando menu_app/fixtures/products.json...
  ✓ menu_app/fixtures/products.json cargado exitosamente.
Cargando menu_app/fixtures/ratings.json...
  ✓ menu_app/fixtures/ratings.json cargado exitosamente.

Proceso completado: 4 fixtures cargados exitosamente, 0 errores.
```

## Configuración del Entorno de Desarrollo

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Cargar datos iniciales
python manage.py loaddata users/fixtures/users.json
python manage.py loaddata menu_app/fixtures/categories.json
python manage.py loaddata menu_app/fixtures/products.json
python manage.py loaddata menu_app/fixtures/ratings.json

# O usar el comando personalizado para cargar todos los fixtures
python manage.py load_all_fixtures

# Iniciar servidor de desarrollo
python manage.py runserver
```

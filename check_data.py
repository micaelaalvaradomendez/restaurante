#!/usr/bin/env python
import os
import sys
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

# Importar modelos después de la configuración
from menu_app.models import Category, Product, Rating
from users.models import User

def check_data():
    print('Verificando datos cargados:')
    
    # Verificar categorías
    print('\nCategorías:')
    for category in Category.objects.all():
        print(f"- {category.name}: {category.description}")

    # Verificar productos
    print('\nProductos:')
    for product in Product.objects.all():
        categories = ", ".join([c.name for c in product.categories.all()])
        print(f"- {product.name} (${product.price}): {product.description}")
        print(f"  Categorías: {categories or 'Sin categorías asignadas'}")

    # Verificar calificaciones
    print('\nCalificaciones:')
    ratings = Rating.objects.all()
    if ratings.exists():
        for rating in ratings:
            print(f"- {rating.user.username} calificó {rating.product.name} con {rating.rating}/5: {rating.title}")
            print(f"  {rating.text}")
    else:
        print('  No hay calificaciones registradas.')

    # Verificar usuarios
    print('\nUsuarios:')
    for user in User.objects.all():
        print(f"- {user.username} ({user.email}): {user.rol}")

if __name__ == '__main__':
    check_data()

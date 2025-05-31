from django.core.management.base import BaseCommand
from menu_app.models import Category, Product, Rating
from users.models import User

class Command(BaseCommand):
    help = 'Verifica los datos cargados en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Verificando datos cargados:'))
        
        # Verificar categorías
        self.stdout.write('\nCategorías:')
        for category in Category.objects.all():
            self.stdout.write(f"- {category.name}: {category.description}")

        # Verificar productos
        self.stdout.write('\nProductos:')
        for product in Product.objects.all():
            categories = ", ".join([c.name for c in product.categories.all()])
            self.stdout.write(f"- {product.name} (${product.price}): {product.description}")
            self.stdout.write(f"  Categorías: {categories or 'Sin categorías asignadas'}")

        # Verificar calificaciones
        self.stdout.write('\nCalificaciones:')
        ratings = Rating.objects.all()
        if ratings.exists():
            for rating in ratings:
                self.stdout.write(f"- {rating.user.username} calificó {rating.product.name} con {rating.rating}/5: {rating.title}")
                self.stdout.write(f"  {rating.text}")
        else:
            self.stdout.write('  No hay calificaciones registradas.')

        # Verificar usuarios
        self.stdout.write('\nUsuarios:')
        for user in User.objects.all():
            self.stdout.write(f"- {user.username} ({user.email}): {user.rol}")

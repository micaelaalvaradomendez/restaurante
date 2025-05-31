from menu_app.models import Category, Product, Rating
from users.models import User

print("Categorías:")
for category in Category.objects.all():
    print(f"- {category.name}: {category.description}")

print("\nProductos:")
for product in Product.objects.all():
    categories = ", ".join([c.name for c in product.categories.all()])
    print(f"- {product.name} (${product.price}): {product.description}")
    print(f"  Categorías: {categories}")

print("\nCalificaciones:")
for rating in Rating.objects.all():
    print(f"- {rating.user.username} calificó {rating.product.name} con {rating.rating}/5: {rating.title}")
    print(f"  {rating.text}")

print("\nUsuarios:")
for user in User.objects.all():
    print(f"- {user.username} ({user.email}): {user.rol}")

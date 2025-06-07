# models/product.py
from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    quantity = models.IntegerField(verbose_name="Cantidad")
    image = models.ImageField(upload_to='productos/', null=True, blank=True, verbose_name="Imagen")
    categories = models.ManyToManyField(Category, related_name='products', verbose_name="Categorías")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    
    def __str__(self):
        # devuelve el nombre si existe, y sino el titulo
        return self.title if self.title else self.name
        
    @classmethod
    def validate(cls, name, description, price):
        errors = {}
        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if description == "":
            errors["description"] = "Por favor ingrese una descripcion"

        if price <= 0:
            errors["price"] = "Por favor ingrese un precio mayor a 0"

        return errors

    @classmethod
    def new(cls, name, description, price, quantity, image=None, categories=None):
        errors = cls.validate(name, description, price)

        if errors:
            return False, errors

        product = cls.objects.create(
            name=name,
            title=name,
            description=description,
            price=price,
            quantity=quantity,
            image=image,
        )

        if categories:
            product.categories.set(categories)

        return True, product

    def update(self, name=None, description=None, price=None, quantity=None, categories=None):
        self.name = name or self.name
        self.title = name or self.title  # Actualizamos ambos campos
        self.description = description or self.description
        self.price = price or self.price
        self.quantity = quantity or self.quantity

        if categories is not None:
            self.categories.set(categories)

        self.save()
        return self

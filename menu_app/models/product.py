# models/product.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    categories = models.ManyToManyField("Category", blank=True)  # relacion muchos a muchos
    is_available = models.BooleanField(default=True)
    
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

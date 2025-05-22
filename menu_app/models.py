from django.db import models
from django.contrib.auth import get_user_model

user=get_user_model()

class Category(models.Model):
    name=models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    title=models.CharField(max_length=100, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    categories= models.ManyToManyField(Category, blank=True) #relacion muchos a muchos
    is_available=models.BooleanField(default=True)
    def __str__(self):
        return self.name or self.title
        #devuelve el nombre si existe, y sino el titulo

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
        errors = Product.validate(name, description, price)

        if errors:
            return False, errors

        Product.objects.create(
            name=name,
            title=name,
            description=description,
            price=price,
            quantity=quantity,
            image=image,
        )

        if categories:
            Product.categories.set(categories)

        return True, Product

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

class Rating(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # 1 calificación por usuario-producto
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"
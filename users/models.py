from django.db import models
from django.contrib.auth.models import AbstractUser

#creacion de los usuarios

class user(AbstractUser):
    Roles = [
        ('ADMIN','Administrador'),
        ('CAJERO','Cajero'),
        ('CLIENTE','Cliente')
    ]
    rol=models.CharField (max_lenght=10,choices=Roles, default='CLIENTE')
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.username
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

#creacion de los usuarios

class User(AbstractUser):
    Roles = [
        ('ADMIN','Administrador'),
        ('CAJERO','Cajero'),
        ('CLIENTE','Cliente')
    ]
    rol=models.CharField (max_length=10,choices=Roles, default='CLIENTE')
    email=models.EmailField(unique=True)

    # Sobrescribir estos campos para evitar conflictos con auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Cambia el related_name para que no choque
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Cambia también aquí
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username
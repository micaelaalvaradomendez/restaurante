from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from menu_app.models import Product, Category, Rating
from django.contrib.auth import get_user_model

print("Iniciando test del modelo menu_app...")

User = get_user_model()

# ------------------- TESTS DE MODELO CATEGORY -------------------
class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Entradas",
            description="Entradas saludables y deliciosas"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Entradas")
        self.assertEqual(self.category.description, "Entradas saludables y deliciosas")
        self.assertTrue(self.category.is_active)
        self.assertEqual(str(self.category), "Entradas")

    def test_category_default_is_active(self):
        new_category = Category.objects.create(
            name="Postres",
            description="Deliciosos postres y dulces"
        )
        self.assertTrue(new_category.is_active)

    def test_category_deactivation(self):
        self.category.is_active = False
        self.category.save()
        self.assertFalse(self.category.is_active)

# ------------------- TESTS DE MODELO PRODUCT -------------------
class ProductModelTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Postres", description="Deliciosos postres y dulces")
        self.category2 = Category.objects.create(name="Bebidas", description="Bebidas refrescantes y saludables")
        self.product = Product.objects.create(
            name="Tiramisú",
            description="Delicioso postre de café",
            price=9000.00,
            quantity=5
        )
        self.product.categories.add(self.category1)
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Tiramisú")
        self.assertEqual(self.product.title, "")  # El modelo deja title vacío si no se asigna
        self.assertEqual(self.product.description, "Delicioso postre de café")
        self.assertEqual(self.product.price, 9000.00)
        self.assertEqual(self.product.quantity, 5)
        self.assertTrue(self.product.is_available)
        self.assertEqual(self.product.categories.count(), 1)
        self.assertEqual(str(self.product), "Tiramisú")  # __str__ usa name si title es vacío

    def test_product_without_title(self):
        product = Product.objects.create(
            name="Café con leche",
            description="Delicioso café con leche",
            price=5000.00,
            quantity=10
        )
        self.assertEqual(product.title, "")  # Espera string vacío si el modelo no autocompleta
        self.assertEqual(str(product), "Café con leche")  # __str__ usa name si title es vacío

    def test_product_with_different_title(self):
        product = Product.objects.create(
            name="Gin tonic",
            title="Gin Tonic Especial",
            description="Delicioso cóctel de ginebra",
            price=8000.00,
            quantity=30
        )
        self.assertEqual(product.title, "Gin Tonic Especial")
        self.assertEqual(str(product), "Gin Tonic Especial")  # __str__ usa title si existe

    def test_product_with_image(self):
        product = Product.objects.create(
            name="Tiramisú",
            description="Tiramisú clásico italiano",
            price=899.99,
            quantity=20,
            image=self.test_image
        )
        self.assertTrue(product.image)

    def test_product_validate_method(self):
        errors = Product.validate("Producto válido", "Descripción válida", 100)
        self.assertEqual(errors, {})
        errors = Product.validate("", "Descripción válida", 100)
        self.assertEqual(errors["name"], "Por favor ingrese un nombre")
        errors = Product.validate("Nombre válido", "", 100)
        self.assertEqual(errors["description"], "Por favor ingrese una descripcion")
        errors = Product.validate("Nombre válido", "Descripción válida", 0)
        self.assertEqual(errors["price"], "Por favor ingrese un precio mayor a 0")
        errors = Product.validate("Nombre válido", "Descripción válida", -10)
        self.assertEqual(errors["price"], "Por favor ingrese un precio mayor a 0")

    def test_product_new_method_success(self):
        success, result = Product.new(
            name="Nuevo producto",
            description="Descripción válida",
            price=100,
            quantity=10
        )
        self.assertTrue(success)
        self.assertIsInstance(result, Product)

    def test_product_new_method_failure(self):
        success, errors = Product.new(
            name="",
            description="",
            price=0,
            quantity=10
        )
        self.assertFalse(success)
        self.assertEqual(len(errors), 3)
        self.assertIn("name", errors)
        self.assertIn("description", errors)
        self.assertIn("price", errors)

    def test_product_update_method(self):
        updated_product = self.product.update(
            name="Torta Matilda",
            price=9000.00,
            categories=[self.category2.id]
        )
        self.assertEqual(updated_product.name, "Torta Matilda")
        self.assertEqual(updated_product.title, "Torta Matilda")
        self.assertEqual(updated_product.price, 9000.00)
        self.assertEqual(updated_product.categories.count(), 1)
        self.assertEqual(updated_product.categories.first(), self.category2)
        original_description = self.product.description
        updated_product = self.product.update(quantity=60)
        self.assertEqual(updated_product.quantity, 60)
        self.assertEqual(updated_product.description, original_description)

# ------------------- TESTS DE MODELO RATING -------------------
class RatingModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpass123')
        self.category = Category.objects.create(name="Meriendas", description="...")
        self.product = Product.objects.create(
            name="Café con leche",
            description="Delicioso café con leche",
            price=799.99,
            quantity=15
        )
        self.product.categories.add(self.category)
        self.rating = Rating.objects.create(
            user=self.user1,
            product=self.product,
            rating=5,
            title="Excelente producto",
            text="La calidad de imagen es increíble"
        )

    def test_rating_creation(self):
        self.assertEqual(self.rating.user, self.user1)
        self.assertEqual(self.rating.product, self.product)
        self.assertEqual(self.rating.rating, 5)
        self.assertEqual(self.rating.title, "Excelente producto")
        self.assertEqual(self.rating.text, "La calidad de imagen es increíble")
        self.assertEqual(str(self.rating), "user1 - Café con leche (5/5)")

    def test_rating_unique_together(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Rating.objects.create(
                user=self.user1,
                product=self.product,
                rating=4,
                title="Buen producto",
                text="Podría mejorar"
            )

    def test_multiple_ratings_for_different_users(self):
        Rating.objects.create(
            user=self.user2,
            product=self.product,
            rating=4,
            title="Muy bueno",
            text="Mejor de lo esperado"
        )
        ratings = Rating.objects.filter(product=self.product)
        self.assertEqual(ratings.count(), 2)

    def test_rating_choices(self):
        rating = Rating.objects.create(
            user=self.user2,
            product=self.product,
            rating=3,
            title="Regular",
            text="Ni bueno ni malo"
        )
        self.assertEqual(rating.rating, 3)
        from django.core.exceptions import ValidationError
        rating = Rating(
            user=self.user2,
            product=self.product,
            rating=6,
            title="Invalido",
            text="Rating fuera de rango"
        )
        with self.assertRaises(ValidationError):
            rating.full_clean()

    def test_rating_verbose_names(self):
        meta = Rating._meta
        self.assertEqual(meta.verbose_name, 'Calificación')
        self.assertEqual(meta.verbose_name_plural, 'Calificaciones')

# ------------------- TESTS DE PRODUCTO BÁSICO -------------------
class BasicProductModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Entradas", description="Entradas frías")
        self.product = Product.objects.create(
            name="Ensalada",
            description="Ensalada fresca",
            price=100,
            quantity=10,
            is_available=True
        )
        self.product.categories.add(self.cat)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Ensalada")

    def test_product_category_relation(self):
        self.assertIn(self.cat, self.product.categories.all())

    def test_product_validation(self):
        errors = Product.validate("", "", -5)
        self.assertIn("name", errors)
        self.assertIn("description", errors)
        self.assertIn("price", errors)

# ------------------- TESTS DE VISTAS -------------------
class MenuViewsTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Platos", description="Platos principales")
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        self.product = Product.objects.create(
            name="Milanesa",
            description="Milanesa con papas",
            price=200,
            quantity=5,
            is_available=True,
            image=self.test_image  # <-- Agrega imagen
        )
        self.product.categories.add(self.cat)

    def test_menu_por_categorias_view_status(self):
        url = reverse('menu_por_categorias')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Platos")
        self.assertContains(response, "Milanesa")

    def test_product_detail_view(self):
        url = reverse('product_detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milanesa")

# ------------------- TESTS DE TEMPLATES -------------------
class TemplateTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Platos", description="Platos principales")
        self.product = Product.objects.create(
            name="Milanesa",
            description="Milanesa con papas",
            price=200,
            quantity=5,
            is_available=True
        )
        self.product.categories.add(self.cat)

    def test_home_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, "home.html")

    def test_menu_template_used(self):
        response = self.client.get(reverse("menu_por_categorias"))
        self.assertTemplateUsed(response, "menu/menu_por_categorias.html")

    def test_product_detail_template_used(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertTemplateUsed(response, "menu/product_detail.html")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\n Finalizaron los tests del modelo menu_app...")
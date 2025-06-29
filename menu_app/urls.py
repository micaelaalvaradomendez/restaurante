from django.urls import path
from .views import HomeView, MenuListView, ProductDetailView, MenuPorCategoriasView
from .views.rating import RatingCreateView, RatingUpdateView, RatingDeleteView
from . import views

urlpatterns = [ 
    path("", HomeView.as_view(), name="home"),
    path("menu/", MenuPorCategoriasView.as_view(), name="menu_por_categorias"),
    path("menu/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path('calificar/<int:product_id>/', RatingCreateView.as_view(), name='calificar_producto'),
    path('calificacion/<int:pk>/editar/', RatingUpdateView.as_view(), name='editar_calificacion'),
    path('calificacion/<int:pk>/eliminar/', RatingDeleteView.as_view(), name='eliminar_calificacion'),
    path('favoritos/agregar/<int:product_id>/', views.add_favorite, name='add_favorite'),
    path('favoritos/quitar/<int:product_id>/', views.remove_favorite, name='remove_favorite'),
]
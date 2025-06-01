# views/product_detail_view.py
from django.views.generic import DetailView
from ..models import Product

class ProductDetailView(DetailView):
    model = Product
    template_name = "menu/product_detail.html"
    context_object_name = "product"

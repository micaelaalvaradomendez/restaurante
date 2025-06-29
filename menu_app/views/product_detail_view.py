from django.views.generic import DetailView, ListView
from django.db.models import Case, When, Value, IntegerField
from ..models import Product
from menu_app.models.favorite import Favorite

class ProductDetailView(DetailView):
    model = Product
    template_name = "menu/product_detail.html"
    context_object_name = "product"

class ProductListView(ListView):
    model = Product
    template_name = "menu_app/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.all()
        if self.request.user.is_authenticated:
            favoritos = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            qs = qs.annotate(
                is_fav=Case(
                    When(id__in=favoritos, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            ).order_by('is_fav', 'name')
        return qs

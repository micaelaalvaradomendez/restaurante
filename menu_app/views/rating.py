from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..models import Rating, Product
from orders.models import OrderItem

class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    fields = ['rating', 'title', 'text']
    template_name = "menu/rating_product.html"

    def dispatch(self, request, *args, **kwargs):
        self.product = Product.objects.get(pk=self.kwargs['product_id'])
        # Solo puede calificar si pidió el producto alguna vez
        if not OrderItem.objects.filter(order__user=request.user, product=self.product).exists():
            messages.error(request, "Solo puedes calificar productos que hayas pedido.")
            return redirect('product_detail', pk=self.product.id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('perfil')

class RatingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rating
    fields = ['rating', 'title', 'text']
    template_name = "menu/rating_product.html"

    def test_func(self):
        rating = self.get_object()
        return rating.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('perfil')

class RatingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rating
    template_name = "menu/rating_confirm_delete.html"

    def test_func(self):
        rating = self.get_object()
        return rating.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('perfil')
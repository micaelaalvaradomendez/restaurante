from django import forms
from orders.models import OrderItem
from menu_app.models import Product

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price_at_purchase']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_available=True)
        self.fields['price_at_purchase'].widget.attrs['readonly'] = True
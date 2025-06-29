from django import forms
from orders.models import OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price_at_purchase']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price_at_purchase'].widget.attrs['readonly'] = True
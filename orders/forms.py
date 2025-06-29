from django import forms

class PaymentForm(forms.Form):
    cardholder_name = forms.CharField(
        label="Nombre del titular",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan Perez'})
    )
    card_number = forms.CharField(
        label="Número de la tarjeta",
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '**** **** **** ****'})
    )
    expiration_date = forms.CharField(
        label="Fecha de vencimiento (MM/AA)",
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12/25'})
    )
    cvv = forms.CharField(
        label="CVV",
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'})
    )
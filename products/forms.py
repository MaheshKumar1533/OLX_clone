from django import forms
from .models import Product, ProductImage, Contact
from categories.models import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price', 'category', 'condition',
            'city', 'state', 'country', 'brand', 'model', 'is_negotiable'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        
        # Add CSS classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ProductSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search products...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min Price',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max Price',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'form-control'
        })
    )
    condition = forms.ChoiceField(
        choices=[('', 'All Conditions')] + Product.CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ContactSellerForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['message', 'buyer_phone', 'buyer_email']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your message to the seller...',
                'class': 'form-control'
            }),
            'buyer_phone': forms.TextInput(attrs={
                'placeholder': 'Your phone number',
                'class': 'form-control'
            }),
            'buyer_email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['buyer_email'].initial = user.email
            if hasattr(user, 'profile') and user.profile.phone:
                self.fields['buyer_phone'].initial = user.profile.phone

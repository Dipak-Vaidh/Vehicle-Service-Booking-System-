from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Booking , CarModel

# class SignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         exclude = ['user', 'status', 'created_at']

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         exclude = ['user', 'status', 'created_at']
#         widgets = {
#             'service_date': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control'
#             }),
#             'car_brand': forms.Select(attrs={'class': 'form-control'}),
#             'car_model': forms.Select(attrs={'class': 'form-control'}),
#             'fuel_type': forms.Select(attrs={'class': 'form-control'}),
#             'service_type': forms.Select(attrs={'class': 'form-control'}),
#         }

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         exclude = ['user', 'status', 'created_at']
#         widgets = {
#             'customer_name': forms.TextInput(attrs={
#                 'class': 'form-control'
#             }),
#             'phone': forms.TextInput(attrs={
#                 'class': 'form-control'
#             }),
#             'car_brand': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'car_model': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'fuel_type': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'service_type': forms.Select(attrs={
#                 'class': 'form-control'
#             }),
#             'service_date': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control'
#             }),
#         }

# =================================================== = = = = =  >>>
class BookingForm(forms.ModelForm):


    class Meta:
        model = Booking
        exclude = ['user', 'status', 'created_at']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'car_brand': forms.Select(attrs={'class': 'form-control'}),
            'car_model': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'service_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initially empty
        self.fields['car_model'].queryset = CarModel.objects.none()

        # When brand selected in POST
        if 'car_brand' in self.data:
            try:
                brand_id = int(self.data.get('car_brand'))
                self.fields['car_model'].queryset = CarModel.objects.filter(brand_id=brand_id)
            except (ValueError, TypeError):
                pass

        # When editing existing booking
        elif self.instance.pk:
            self.fields['car_model'].queryset = CarModel.objects.filter(
                brand=self.instance.car_brand
            )
        

   
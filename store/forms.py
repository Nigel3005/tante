from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput
from django import forms
from store.models import Product


# creating a form
class ProductForm(forms.ModelForm):
    # create metaclass
    class Meta:
        # specify model to be used
        model = Product

        # specify fields to be used
        # It includes all the fields of model
        fields = '__all__'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', max_length=254, help_text='Required. Inform a valid email address.',
                             widget=TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'}))
    username = forms.CharField(label='',
                               widget=TextInput(attrs={'placeholder': 'Gebruikersnaam', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='',
                                widget=PasswordInput(attrs={'placeholder': 'Wachtwoord', 'autocomplete': 'off'}))
    password2 = forms.CharField(label='', widget=PasswordInput(
        attrs={'placeholder': 'Herhaal wachtwoord', 'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

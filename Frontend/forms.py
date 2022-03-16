from django import forms
from django.forms import ModelForm
from Frontend.models import GeeksModel


# creating a form
class GeeksForm(forms.ModelForm):

    # create meta class
    class Meta:
    # specify model to be used
        model = GeeksModel

        # specify fields to be used
        fields = '__all__'

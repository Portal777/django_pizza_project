from django import forms
from .models import Pizza, Topping


class MakePizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('title', 'description', 'image', 'recipe')

        widgets = {'recipe': forms.SelectMultiple()}


class MakeToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = '__all__'





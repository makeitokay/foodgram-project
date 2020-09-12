from django import forms

from .models import Recipe


class RecipeCreationForm(forms.ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ("name", "photo", "description", "cooking_time")

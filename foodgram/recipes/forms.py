from django import forms

from .models import Recipe


class RecipeCreationForm(forms.ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ("name", "photo", "description", "cooking_time")

    def clean_cooking_time(self):
        data = self.cleaned_data['cooking_time']
        if not 0 < data < 44640:
            raise forms.ValidationError(
                'Введите корректное время приготовления рецепта.'
            )
        return data

from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import RecipeCreationForm
from .models import Tag, Ingredient, RecipeIngredients
from .utils import filter_by_key


class RecipeCreationView(FormView):
    form_class = RecipeCreationForm
    template_name = 'recipe_creation.html'
    success_url = '/'

    def form_valid(self, form):
        print(form.data)
        # Поля name, photo, description, cooking_time сохранятся тут
        recipe = form.save()
        # А тэги и ингредиенты сохраним отдельно как m2m поля
        for tag in Tag.objects.all():
            if form.data.get(tag.name) is not None:
                recipe.tags.add(tag)

        names = filter_by_key(form.data, 'nameIngredient')
        values = filter_by_key(form.data, 'valueIngredient')
        items = zip(names, values)
        for item in items:
            ingredient = Ingredient.objects.get(name=item[0])
            RecipeIngredients.objects.create(amount=int(item[1]), recipe=recipe, ingredient=ingredient)

        return redirect(self.success_url)

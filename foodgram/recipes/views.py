from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView, ListView

from .forms import RecipeCreationForm
from .models import Tag, Ingredient, RecipeIngredients, Recipe
from .utils import filter_by_key


class RecipeCreationView(LoginRequiredMixin, FormView):
    form_class = RecipeCreationForm
    template_name = 'recipe_creation.html'
    success_url = '/'

    def form_valid(self, form):
        print(form.data)
        # Поля author, name, photo, description, cooking_time сохранятся тут
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()
        # А тэги и ингредиенты сохраним отдельно как m2m поля
        for tag in Tag.objects.all():
            if form.data.get(tag.name) is not None:
                recipe.tags.add(tag)

        names = filter_by_key(form.data, 'nameIngredient')
        values = filter_by_key(form.data, 'valueIngredient')
        items = zip(names, values)
        for item in items:
            ingredient = Ingredient.objects.get(name=item[0])
            RecipeIngredients.objects.create(
                amount=int(item[1]) if item[1] else None,
                recipe=recipe,
                ingredient=ingredient
            )

        return redirect(self.success_url)


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'indexNotAuth.html'
    paginate_by = 6

from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import RecipeCreationForm
from .models import Tag


class RecipeCreationView(FormView):
    form_class = RecipeCreationForm
    template_name = 'recipe_creation.html'
    success_url = '/'

    def form_valid(self, form):
        # Поля name, photo, description, cooking_time сохранятся тут
        recipe = form.save()
        # А тэги и ингредиенты сохраним отдельно как m2m поля
        for tag in Tag.objects.all():
            if form.data.get(tag.name) is not None:
                recipe.tags.add(tag)
        # TODO: добавление ингредиентов
        return redirect(self.success_url)

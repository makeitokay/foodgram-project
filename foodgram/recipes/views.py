from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, ListView, UpdateView, DetailView

from .forms import RecipeCreationForm
from .models import Recipe
from .mixins import RecipeAuthorOnlyMixin

from accounts.models import Favorite


class RecipeCreationView(LoginRequiredMixin, FormView):
    form_class = RecipeCreationForm
    template_name = 'formRecipe.html'
    success_url = '/'

    def form_valid(self, form):
        # Поля author, name, photo, description, cooking_time сохранятся тут
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()
        # А тэги и ингредиенты сохраним отдельно как m2m поля
        recipe.create_m2m_fields(form.data)

        return redirect(self.success_url)


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            favorites = [e[0] for e in Favorite.objects.filter(user=self.request.user).values_list('recipe')]
            context['favorites'] = favorites

        context['tags'] = self.request.GET.get('tags', '')

        return context

    def get_queryset(self):
        tags = self.request.GET.get('tags', '')
        if tags:
            queryset = Recipe.objects.filter(tags__name__in=tags.split(',')).distinct()
        else:
            queryset = Recipe.objects.all()
        return queryset.order_by('-id').prefetch_related('author', 'tags').all()


class RecipeUpdateView(LoginRequiredMixin, RecipeAuthorOnlyMixin, UpdateView):
    model = Recipe
    template_name = 'formChangeRecipe.html'
    fields = ('name', 'photo', 'description', 'cooking_time')
    template_name_field = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = [obj[0] for obj in self.object.tags.values_list('name')]
        context['tags'] = tags
        return context

    def form_valid(self, form):
        recipe = form.save()

        # Удалим все тэги и ингредиенты, а затем добавим новые
        recipe.tags.clear()
        recipe.ingredient_amounts.all().delete()

        recipe.create_m2m_fields(form.data)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recipe-detail', kwargs={'slug': self.object.slug})


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'
    template_name_field = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(user=self.request.user, recipe=self.object).exists()
            context['is_favorite'] = is_favorite
        return context

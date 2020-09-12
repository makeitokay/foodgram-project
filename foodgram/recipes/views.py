from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, ListView, UpdateView, DetailView
from django.views import View
from django.core.cache import cache

from .forms import RecipeCreationForm
from .models import Recipe
from .mixins import RecipeAuthorOnlyMixin


class RecipeCreationView(LoginRequiredMixin, FormView):
    form_class = RecipeCreationForm
    template_name = "formRecipe.html"
    success_url = "/"

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
    context_object_name = "recipes"
    template_name = "index.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            favorites = self.request.user.favorites.values_list("recipe", flat=True)
            context["favorites"] = favorites
            purchases = self.request.user.purchases.values_list("recipe", flat=True)
            context["purchases"] = purchases

        context["tags"] = self.request.GET.get("tags", "")

        return context

    def get_queryset(self):
        tags = self.request.GET.get("tags", "")

        queryset = (
            Recipe.filter_by_tags(tags)
            .order_by("-id")
            .select_related("author")
            .prefetch_related("tags")
            .all()
        )
        return queryset


class RecipeUpdateView(LoginRequiredMixin, RecipeAuthorOnlyMixin, UpdateView):
    model = Recipe
    template_name = "formChangeRecipe.html"
    fields = ("name", "photo", "description", "cooking_time")
    template_name_field = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = self.object.tags.values_list("name", flat=True)
        context["tags"] = tags
        return context

    def form_valid(self, form):
        recipe = form.save()

        # Удалим все тэги и ингредиенты, а затем добавим новые
        recipe.tags.clear()
        recipe.ingredient_amounts.all().delete()

        recipe.create_m2m_fields(form.data)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("recipe-detail", kwargs={"slug": self.object.slug})


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "singlePage.html"
    template_name_field = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            is_favorite = self.request.user.favorites.filter(
                recipe=self.object
            ).exists()
            is_following = self.request.user.following.filter(
                following=self.object.author
            ).exists()
            is_purchased = self.request.user.purchases.filter(
                recipe=self.object
            ).exists()
            context["is_favorite"] = is_favorite
            context["is_following"] = is_following
            context["is_purchased"] = is_purchased
        return context


class RecipeDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=kwargs.get("slug"))
        if recipe.author != request.user:
            raise PermissionDenied()
        recipe.delete()
        return redirect(reverse("recipe-list"))

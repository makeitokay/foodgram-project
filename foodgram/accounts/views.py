from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.views.generic import ListView
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from recipes.models import Recipe


class FavoriteRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "favorite.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = self.request.GET.get("tags", "")
        purchases = self.request.user.purchases.values_list(
            "recipe", flat=True
        )
        context["purchases"] = purchases
        return context

    def get_queryset(self):
        tags = self.request.GET.get("tags", "")
        queryset = Recipe.objects.filter_by_tags(tags).filter(
            favorite_objects__user=self.request.user
        )
        return queryset.select_related(
            "author"
        ).prefetch_related(
            "tags"
        ).all()


class AuthorRecipeListView(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "authorRecipe.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            favorites = self.request.user.favorites.values_list(
                "recipe", flat=True
            )
            purchases = self.request.user.purchases.values_list(
                "recipe", flat=True
            )
            is_following = self.request.user.following.filter(
                following=self.kwargs.get("pk")
            ).exists()
            context["purchases"] = purchases
            context["is_following"] = is_following
            context["favorites"] = favorites

        context["author"] = get_object_or_404(User, pk=self.kwargs.get("pk"))
        context["tags"] = self.request.GET.get("tags", "")

        return context

    def get_queryset(self):
        tags = self.request.GET.get("tags", "")
        queryset = Recipe.objects.filter_by_tags(tags)
        queryset = queryset.filter(author=self.kwargs.get("pk"))
        return queryset.select_related(
            "author"
        ).prefetch_related(
            "tags"
        ).all()


class FollowingAuthorsListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "authors"
    template_name = "myFollow.html"
    paginate_by = 6

    def get_queryset(self):
        authors = User.objects.filter(
            followers__user=self.request.user
        ).annotate(
            recipe_count=Count("recipes") - 3
        ).all()
        return authors


class PurchasesListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = "purchases"
    template_name = "shopList.html"

    def get_queryset(self):
        return Recipe.objects.filter(purchases__user=self.request.user).all()


class DownloadPurchaseListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.filter(
            purchases__user=self.request.user
        ).prefetch_related(
            "ingredient_amounts"
        ).all()
        ingredients = {}
        ingredients_by_taste = []
        for recipe in recipes:
            for obj in recipe.ingredient_amounts.select_related(
                    "ingredient"
            ).all():
                ing = obj.ingredient
                if ing.unit == "по вкусу":
                    ingredients_by_taste.append(ing.name)
                    continue
                if ing.name not in ingredients:
                    ingredients[ing.name] = {
                        "unit": ing.unit,
                        "amount": float(obj.amount),
                    }
                    continue
                ingredients[ing.name]["amount"] += float(obj.amount)
        output = ""
        for k, v in ingredients.items():
            output += f"{k} - {v['amount']} {v['unit']}.\n"
        if ingredients_by_taste:
            output += ", ".join(ingredients_by_taste) + " - по вкусу\n\n"
        output += "Список скачан с помощью продуктового помощника Foodgram."

        filename = "result.txt"
        response = HttpResponse(output, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename={0}".format(
            filename
        )

        return response

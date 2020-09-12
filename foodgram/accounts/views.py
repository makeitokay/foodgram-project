from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import FileResponse, HttpResponse
from django.views.generic import ListView
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import io

from recipes.models import Recipe
from .models import Favorite, Follow, Purchase


class FavoriteRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'favorite.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.request.GET.get('tags', '')
        purchases = self.request.user.purchases.values_list('recipe', flat=True)
        context['purchases'] = purchases
        return context

    def get_queryset(self):
        tags = self.request.GET.get('tags', '')
        favorites = self.request.user.favorites.values_list('recipe', flat=True)
        queryset = Recipe.filter_by_tags(tags)
        queryset = queryset.filter(pk__in=favorites)
        return queryset.order_by('-id').prefetch_related('author', 'tags').all()


class AuthorRecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'authorRecipe.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            favorites = self.request.user.favorites.values_list('recipe', flat=True)
            purchases = self.request.user.purchases.values_list('recipe', flat=True)
            is_following = self.request.user.following.filter(following=self.kwargs.get('pk')).exists()
            context['purchases'] = purchases
            context['is_following'] = is_following
            context['favorites'] = favorites

        context['author'] = get_object_or_404(User, pk=self.kwargs.get('pk'))
        context['tags'] = self.request.GET.get('tags', '')

        return context

    def get_queryset(self):
        tags = self.request.GET.get('tags', '')
        queryset = Recipe.filter_by_tags(tags)
        queryset = queryset.filter(author=self.kwargs.get('pk'))
        return queryset.order_by('-id').select_related('author').prefetch_related('tags').all()


class FollowingAuthorsListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'authors'
    template_name = 'myFollow.html'
    paginate_by = 6

    def get_queryset(self):
        following = self.request.user.following.values_list('following', flat=True)
        authors = User.objects.filter(pk__in=following).annotate(recipe_count=Count('recipes') - 3).all()
        return authors


class PurchasesListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'purchases'
    template_name = 'shopList.html'

    def get_queryset(self):
        recipes_id = self.request.user.purchases.values_list('recipe', flat=True)
        recipes = Recipe.objects.filter(pk__in=recipes_id).all()
        return recipes


class DownloadPurchaseListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        recipes_id = self.request.user.purchases.values_list('recipe', flat=True)
        recipes = Recipe.objects.filter(pk__in=recipes_id).prefetch_related('ingredient_amounts').all()
        ingredients = {}
        ingredients_by_taste = []
        for recipe in recipes:
            for obj in recipe.ingredient_amounts.select_related('ingredient').all():
                ing = obj.ingredient
                if ing.unit == 'по вкусу':
                    ingredients_by_taste.append(ing.name)
                    continue
                if ing.name not in ingredients:
                    ingredients[ing.name] = {'unit': ing.unit, 'amount': float(obj.amount)}
                    continue
                ingredients[ing.name]['amount'] += float(obj.amount)
        output = ""
        for k, v in ingredients.items():
            output += f"{k} - {v['amount']} {v['unit']}.\n"
        output += ', '.join(ingredients_by_taste) + " - по вкусу\n\n"
        output += "Список скачан с помощью продуктового помощника Foodgram."

        filename = 'result.txt'
        response = HttpResponse(output, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

        return response

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

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
        purchases = Purchase.objects.filter(user=self.request.user).values_list('recipe', flat=True)
        context['purchases'] = purchases
        return context

    def get_queryset(self):
        tags = self.request.GET.get('tags', '')
        favorites = Favorite.objects.filter(user=self.request.user).values_list('recipe', flat=True)
        if tags:
            queryset = Recipe.objects.filter(tags__name__in=tags.split(',')).distinct()
        else:
            queryset = Recipe.objects.all()
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
            favorites = [e[0] for e in Favorite.objects.filter(user=self.request.user).values_list('recipe')]
            purchases = Purchase.objects.filter(user=self.request.user).values_list('recipe', flat=True)
            is_following = Follow.objects.filter(user=self.request.user, following=self.kwargs.get('pk')).exists()
            context['purchases'] = purchases
            context['is_following'] = is_following
            context['favorites'] = favorites

        context['author'] = get_object_or_404(User, pk=self.kwargs.get('pk'))
        context['tags'] = self.request.GET.get('tags', '')

        return context

    def get_queryset(self):
        tags = self.request.GET.get('tags', '')
        if tags:
            queryset = Recipe.objects.filter(tags__name__in=tags.split(',')).distinct()
        else:
            queryset = Recipe.objects.all()
        queryset = queryset.filter(author=self.kwargs.get('pk'))
        return queryset.order_by('-id').prefetch_related('author', 'tags').all()


class FollowingAuthorsListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'authors'
    template_name = 'myFollow.html'
    paginate_by = 6

    def get_queryset(self):
        following = Follow.objects.filter(user=self.request.user).values_list('following', flat=True)
        authors = User.objects.filter(pk__in=following).annotate(recipe_count=Count('recipes') - 3).all()
        return authors

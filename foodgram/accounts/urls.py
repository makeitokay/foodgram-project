from django.urls import path, include
from . import views

urlpatterns = [
    path('favorites/', views.FavoriteRecipeListView.as_view(), name='favorite-list'),
    path('<int:pk>/', views.AuthorRecipeListView.as_view(), name='author-recipe-list'),
]

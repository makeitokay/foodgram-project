from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.RecipeCreationView.as_view(), name="recipe-creation"),
    path("<slug>/edit/", views.RecipeUpdateView.as_view(), name="recipe-update"),
    path("<slug>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("<slug>/delete/", views.RecipeDeleteView.as_view(), name="recipe-delete"),
    path("", views.RecipeListView.as_view(), name="recipe-list"),
]

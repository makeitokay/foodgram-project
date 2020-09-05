from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.RecipeCreationView.as_view(), name='recipe-creation'),
]
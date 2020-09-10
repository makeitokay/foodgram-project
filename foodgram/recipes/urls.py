from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.RecipeCreationView.as_view(), name='recipe-creation'),
    path('<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('<slug>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('', views.RecipeListView.as_view(), name='recipe-list')
]

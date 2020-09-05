from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredients/', views.IngredientListView.as_view(), name='ingredients-list'),
]

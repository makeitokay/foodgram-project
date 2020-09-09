from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredients/', views.IngredientListView.as_view(), name='ingredients-list'),
    path('favorites/', views.CreateFavoriteView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/', views.DestroyFavoriteView.as_view(), name='favorite-destroy')
]

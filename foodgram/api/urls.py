from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredients/', views.IngredientListView.as_view(), name='ingredients-list'),
    path('favorites/', views.CreateFavoriteView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/', views.DeleteFavoriteView.as_view(), name='favorite-delete'),
    path('subscriptions/', views.CreateFollowView.as_view(), name='follow-create'),
    path('subscriptions/<int:pk>/', views.DeleteFollowView.as_view(), name='follow-delete'),
]

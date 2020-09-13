from django.urls import path
from . import views

urlpatterns = [
    path("ingredients/", views.IngredientListView.as_view(), name="ingredients-list"),
    path("favorites/", views.CreateFavoriteView.as_view(), name="favorite-create"),
    path(
        "favorites/<int:pk>/",
        views.DeleteFavoriteView.as_view(),
        name="favorite-delete",
    ),
    path("subscriptions/", views.CreateFollowView.as_view(), name="follow-create"),
    path(
        "subscriptions/<int:pk>/",
        views.DeleteFollowView.as_view(),
        name="follow-delete",
    ),
    path("purchases/", views.CreatePurchaseView.as_view(), name="purchase-create"),
    path(
        "purchases/<int:pk>/",
        views.DeletePurchaseView.as_view(),
        name="purchase-delete",
    ),
]

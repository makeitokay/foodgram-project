from django.urls import path
from . import views

urlpatterns = [
    path("favorites/", views.FavoriteRecipeListView.as_view(), name="favorite-list"),
    path("<int:pk>/", views.AuthorRecipeListView.as_view(), name="author-recipe-list"),
    path("following/", views.FollowingAuthorsListView.as_view(), name="following-list"),
    path("purchases/", views.PurchasesListView.as_view(), name="purchase-list"),
    path(
        "purchases/download",
        views.DownloadPurchaseListView.as_view(),
        name="purchase-list-download",
    ),
]

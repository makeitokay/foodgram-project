from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .serializers import (
    IngredientListSerializer,
    FavoriteSerializer,
    FollowSerializer,
    PurchaseSerializer,
)
from recipes.models import Ingredient
from accounts.models import Favorite, Follow, Purchase


class IngredientListView(ListAPIView):
    serializer_class = IngredientListSerializer
    model = Ingredient

    def get_queryset(self):
        if "query" in self.request.query_params:
            return Ingredient.objects.filter(
                name__startswith=self.request.query_params["query"].lower()
            ).all()
        return Ingredient.objects.all()


class CreateFavoriteView(CreateAPIView):
    serializer_class = FavoriteSerializer


class DeleteFavoriteView(APIView):
    def delete(self, request, pk):
        favorite = get_object_or_404(Favorite, user=request.user, recipe=pk)
        favorite.delete()
        return Response({"success": "true"})


class CreateFollowView(CreateAPIView):
    serializer_class = FollowSerializer


class DeleteFollowView(APIView):
    def delete(self, request, pk):
        follow = get_object_or_404(Follow, user=request.user, following=pk)
        follow.delete()
        return Response({"success": "true"})


class CreatePurchaseView(CreateAPIView):
    serializer_class = PurchaseSerializer


class DeletePurchaseView(APIView):
    def delete(self, request, pk):
        purchase = get_object_or_404(Purchase, user=request.user, recipe=pk)
        purchase.delete()
        return Response({"success": "true"})

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .serializers import IngredientListSerializer, FavoriteSerializer, FollowSerializer
from recipes.models import Ingredient
from accounts.models import Favorite, Follow


class IngredientListView(ListAPIView):
    serializer_class = IngredientListSerializer
    model = Ingredient

    def get_queryset(self):
        if 'query' in self.request.query_params:
            return Ingredient.objects.filter(
                name__startswith=self.request.query_params['query'].lower()
            ).all()
        return Ingredient.objects.all()


class CreateFavoriteView(CreateAPIView):
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteFavoriteView(APIView):
    def delete(self, request, pk):
        favorite = get_object_or_404(Favorite, user=request.user, recipe=pk)
        favorite.delete()
        return Response({'success': 'true'})


class CreateFollowView(CreateAPIView):
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteFollowView(APIView):
    def delete(self, request, pk):
        follow = get_object_or_404(Follow, user=request.user, following=pk)
        follow.delete()
        return Response({'success': 'true'})

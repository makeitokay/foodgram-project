from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IngredientListSerializer, FavoriteSerializer
from recipes.models import Ingredient
from accounts.models import Favorite


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


class DestroyFavoriteView(APIView):
    def delete(self, request, pk):
        try:
            favorite = Favorite.objects.get(user=request.user, recipe=pk)
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        favorite.delete()
        return Response({'success': 'true'})
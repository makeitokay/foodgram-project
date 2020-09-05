from rest_framework.generics import ListAPIView

from .serializers import IngredientListSerializer
from recipes.models import Ingredient


class IngredientListView(ListAPIView):
    serializer_class = IngredientListSerializer
    model = Ingredient

    def get_queryset(self):
        if 'query' in self.request.query_params:
            return Ingredient.objects.filter(
                name__startswith=self.request.query_params['query'].lower()
            ).all()
        return Ingredient.objects.all()

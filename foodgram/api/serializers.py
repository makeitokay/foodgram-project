from rest_framework import serializers

from recipes.models import Ingredient
from accounts.models import Favorite


class IngredientListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    dimension = serializers.CharField(source='unit')

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ('user',)
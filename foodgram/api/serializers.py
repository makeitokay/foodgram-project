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
        fields = ('user', 'recipe')
        read_only_fields = ('user',)

    def validate_recipe(self, value):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, recipe=value).exists():
            return serializers.ValidationError('Favorite already exists')
        return value

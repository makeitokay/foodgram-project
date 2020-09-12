from rest_framework import serializers

from recipes.models import Ingredient
from accounts.models import Favorite, Follow, Purchase


class IngredientListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="name")
    dimension = serializers.CharField(source="unit")

    class Meta:
        model = Ingredient
        fields = ("title", "dimension")


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        read_only_fields = ("user",)

    def validate_recipe(self, value):
        user = self.context["request"].user
        if Favorite.objects.filter(user=user, recipe=value).exists():
            return serializers.ValidationError("Favorite already exists")
        return value


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("user", "following")
        read_only_fields = ("user",)

    def validate_following(self, value):
        user = self.context["request"].user
        if Follow.objects.filter(user=user, following=value).exists():
            raise serializers.ValidationError("Following already exists")
        if user == value:
            raise serializers.ValidationError("You can't follow to yourself")
        return value


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("user", "recipe")
        read_only_fields = ("user",)

    def validate_recipe(self, value):
        user = self.context["request"].user
        if Purchase.objects.filter(user=user, recipe=value).exists():
            return serializers.ValidationError("Purchase already exists")
        return value

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient
from accounts.models import Favorite, Follow, Purchase


class IngredientListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="name")
    dimension = serializers.CharField(source="unit")

    class Meta:
        model = Ingredient
        fields = ("title", "dimension")


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        read_only_fields = ("user",)
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ("user", "following")
        read_only_fields = ("user",)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, value):
        user = self.context["request"].user
        if user == value:
            raise serializers.ValidationError("You can't follow to yourself")
        return value


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Purchase
        fields = ("user", "recipe")
        read_only_fields = ("user",)
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=['user', 'recipe']
            )
        ]

from django.db import models
from django.conf import settings


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites",
    )
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="favorite_objects"
    )

    def __str__(self):
        return f"{self.user.username} -> {self.recipe.name}"


class Follow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )

    def __str__(self):
        return f"{self.user.username} -> {self.following.username}"


class Purchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases"
    )
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.recipe.name}"

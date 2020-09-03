from django.db import models
from django.conf import settings

from foodgram.recipes.utils import russian_slugify


class Ingredient(models.Model):
    name = models.CharField(max_length=40)
    unit = models.CharField(max_length=10)


class RecipeIngredients(models.Model):
    amount = models.DecimalField()
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=15)


class Recipe(models.Model):
    TAG_CHOICES = (
        (0, 'Завтрак'),
        (1, 'Обед'),
        (2, 'Ужин')
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="recipes",
    )
    name = models.CharField(max_length=60)
    photo = models.ImageField(upload_to='recipes/')
    description = models.TextField()
    ingredients = models.ManyToManyField('Ingredient', related_name='recipes',
                                         through='RecipeIngredients')
    tags = models.ManyToManyField('Tag', related_name='recipes')
    cooking_time = models.IntegerField()
    slug = models.SlugField(unique=True, null=False)

    def save(self, *args, **kwargs):
        self.slug = russian_slugify(self.name)
        super().save(*args, **kwargs)

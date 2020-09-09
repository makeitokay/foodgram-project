from django.db import models
from django.conf import settings

from .utils import russian_slugify, filter_by_key


class Ingredient(models.Model):
    name = models.CharField(max_length=70)
    unit = models.CharField(max_length=10)


class RecipeIngredients(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='ingredient_amounts')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ingredient_amounts')


class Tag(models.Model):
    name = models.CharField(max_length=15)
    display_name = models.CharField(max_length=30)
    display_color = models.CharField(max_length=30)


class Recipe(models.Model):
    TAG_CHOICES = (
        (0, 'Завтрак'),
        (1, 'Обед'),
        (2, 'Ужин')
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recipes",
    )
    name = models.CharField(max_length=60)
    photo = models.ImageField(upload_to='recipes/', default='recipes/default.png', null=False)
    description = models.TextField()
    ingredients = models.ManyToManyField('Ingredient', related_name='recipes',
                                         through='RecipeIngredients')
    tags = models.ManyToManyField('Tag', related_name='recipes')
    cooking_time = models.IntegerField()
    slug = models.SlugField(unique=True, null=False)

    def save(self, *args, **kwargs):
        self.slug = russian_slugify(self.name)
        super().save(*args, **kwargs)

    def create_m2m_fields(self, form_data):
        for tag in Tag.objects.all():
            if form_data.get(tag.name) is not None:
                self.tags.add(tag)

        names = filter_by_key(form_data, 'nameIngredient')
        values = filter_by_key(form_data, 'valueIngredient')
        items = zip(names, values)
        for item in items:
            ingredient = Ingredient.objects.get(name=item[0])
            RecipeIngredients.objects.create(
                amount=round(float(item[1].replace(',', '.')), 2) if item[1] else None,
                recipe=self,
                ingredient=ingredient
            )

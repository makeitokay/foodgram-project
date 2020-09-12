from django.db import models
from django.conf import settings

from .utils import russian_slugify, filter_by_key


class Ingredient(models.Model):
    name = models.CharField(max_length=70)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='ingredient_amounts')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ingredient_amounts')


class Tag(models.Model):
    name = models.CharField(max_length=15, db_index=True)
    display_name = models.CharField(max_length=30)
    display_color = models.CharField(max_length=30)

    def __str__(self):
        return self.name


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

    @staticmethod
    def filter_by_tags(tags):
        if tags:
            queryset = Recipe.objects.filter(tags__name__in=tags.split(',')).distinct()
        else:
            queryset = Recipe.objects.all()
        return queryset

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = russian_slugify(self.name)
        super().save(*args, **kwargs)

    def create_m2m_fields(self, form_data):
        for tag in Tag.objects.all():
            if form_data.get(tag.name) is not None:
                self.tags.add(tag)

        # Сначала получаем имена ингредиентов, затем вытащим объекты
        ingredients = filter_by_key(form_data, 'nameIngredient')
        ingredient_objects = Ingredient.objects.filter(name__in=ingredients).all()
        # В исходном списке имен заменим все имена на объекты
        for obj in ingredient_objects:
            ingredients[ingredients.index(obj.name)] = obj
        # Теперь вытащим значения количества для ингредиентов
        values = filter_by_key(form_data, 'valueIngredient')
        # И установим соответствие между ингредиентом и количеством
        items = zip(ingredients, values)
        # p.s.: приведенная выше схема нужна для того,
        # чтобы вытащить все нужные ингредиенты одним запросом к БД

        recipe_ingredients = []
        for ingredient, amount in items:
            recipe_ingredients.append(
                RecipeIngredients(
                    amount=round(float(amount.replace(',', '.')), 2) if amount else None,
                    recipe=self,
                    ingredient=ingredient
                )
            )
        # Также одним запросом создаем все ингредиенты нашего рецепта
        RecipeIngredients.objects.bulk_create(recipe_ingredients)

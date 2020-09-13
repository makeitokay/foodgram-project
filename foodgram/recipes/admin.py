from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredients, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    readonly_fields = ("favorite_counter",)
    list_filter = ("name", "author", "tags")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author")

    def favorite_counter(self, obj):
        return obj.favorite_objects.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "unit")
    list_filter = ("name",)
    search_fields = ("name",)


admin.site.register(RecipeIngredients)
admin.site.register(Tag)

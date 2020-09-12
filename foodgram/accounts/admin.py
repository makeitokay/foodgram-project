from django.contrib import admin

from .models import Follow, Purchase, Favorite


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "following")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "recipe")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "recipe")

from django.contrib.auth.mixins import AccessMixin

from .models import Recipe


class RecipeAuthorOnlyMixin(AccessMixin):
    """Verify that the current user is `author` of requested object."""

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        user = request.user
        try:
            Recipe.objects.get(slug=slug, author=user)
            return super().dispatch(request, *args, **kwargs)
        except Recipe.DoesNotExist:
            return self.handle_no_permission()

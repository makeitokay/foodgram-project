from django.contrib.auth.mixins import AccessMixin

from .models import Recipe


class RecipeAuthorOnlyMixin(AccessMixin):
    """Verify that the current user is `author` of requested object."""

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        try:
            Recipe.objects.get(pk=pk, author=user)
            return super().dispatch(request, *args, **kwargs)
        except Recipe.DoesNotExist:
            return self.handle_no_permission()

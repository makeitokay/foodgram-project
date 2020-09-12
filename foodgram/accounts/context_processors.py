from .models import Purchase


def purchases_counter(request):
    if request.user.is_authenticated:
        return {
            'purchases_counter': Purchase.objects.filter(user=request.user).count()
        }
    return {}

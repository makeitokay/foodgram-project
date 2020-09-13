def purchases_counter(request):
    if request.user.is_authenticated:
        return {"purchases_counter": request.user.purchases.count()}
    return {}

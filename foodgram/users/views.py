from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import FoodgramUserCreationForm


class FoodgramLoginView(LoginView):
    redirect_authenticated_user = True


class RegistrationView(FormView):
    form_class = FoodgramUserCreationForm
    template_name = "registration/signup.html"
    redirect_authenticated_user = True
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

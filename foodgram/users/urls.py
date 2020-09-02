from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.FoodgramLoginView.as_view()),
    path('signup/', views.RegistrationView.as_view()),
    path('', include('django.contrib.auth.urls')),
]

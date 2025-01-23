from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:pk>/rate/', views.rate_recipe, name='rate_recipe'),
    path('recipes/', views.recipe_list, name='recipe_list'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('user profile/<username>', views.user_profile, name='user profile'),
    path('recipes by author/<id>/', views.show_users_recipes, name='recipe by author'),
]
from django.urls import path
from . import views
from .views import home_recipes

app_name = 'recipes'

urlpatterns = [
    path('recipe/<id>/', views.recipe_details, name='recipe detail'),
    path('recipe form/', views.recipe_form, name='fill recipe form'),
    path('home/', home_recipes, name='home five random recipes'),
    path('recipes/', views.show_recipes, name='all recipes'),
    path('<id>/edit/', views.edit_recipe, name='edit a recipe'),
    path('<id>/delete/', views.delete_recipe, name='delete the recipe'),
    path('show all/', views.show_recipes, name='all recipes'),
]
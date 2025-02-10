from django import forms
from django.contrib.auth import get_user_model
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['date_published', 'date_modified']


class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['recipe_author','date_published', 'date_modified']
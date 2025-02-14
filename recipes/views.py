import random

from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse

from .forms import RecipeForm, RecipeEditForm
from .models import Recipe
from django.http import HttpResponse
from django.contrib.auth import get_user_model


def recipe_home(request):
    return HttpResponse('Here some recipes')


def show_recipes(request):
    recipe = Recipe.objects.all()
    return render(request, 'recipes/show_all.html', {'recipes': recipe})


def home_recipes(request):
    recipes = list(Recipe.objects.all())
    recipes = random.sample(recipes, 5)
    recipe = Recipe.objects.order_by('?').first()
    return render(request, 'recipes/home_page.html',
                  {'recipes': recipes, 'recipe': recipe})


def recipe_details(request, id):
    context = {'recipe': Recipe.objects.get(id=id)}
    return render(request, 'recipes/recipe_detail.html', context)


def recipe_details_from_hp(request, id):
    context = {'recipe': Recipe.objects.get(id=id)}
    return render(request, 'recipes/recipe_detail_from_hp.html', context)


def recipe_form(request):
    context = {}
    user = get_user_model()
    if user.is_authenticated:
        form = RecipeForm(request.POST or None, request.FILES or None,
                          initial={'recipe_author': get_user_model().username})

        if form.is_valid():
            form.cleaned_data['recipe_author'] = get_user_model().username
            form.save()

            messages.success(request, 'Your recipe has been saved')
        context['form'] = form
        return render(request, 'recipes/recipe_form.html', context)


def edit_recipe(request, id):
    recipe_to_edit = Recipe.objects.filter(id=id).first()

    if request.method == 'POST':
        edit_form = RecipeEditForm(request.POST, request.FILES,
                                   instance=recipe_to_edit)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'You have edit the recipe')
            return redirect('recipe by author')

    else:
        form = RecipeEditForm(instance=recipe_to_edit)
        return render(request,  'recipes/recipe_edited.html',
                      {'object': 'Recipe', 'edit_form': form})


def delete_recipe(request, id):
    recipe_to_delete = Recipe.objects.filter(id=id).first()

    if request.method == 'POST':
        recipe_to_delete.delete()
        messages.success(request,  'You have deleted the recipe')
        return redirect('/recipe by author')

    else:
        return (render(request,
                       'recipes/confirm_recipe_deletion.html',
                      {'object': 'Recipe',
                       'recipe_to_delete': recipe_to_delete}))

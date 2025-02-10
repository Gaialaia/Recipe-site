from gc import get_objects

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate

from recipes.models import Recipe
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


# password for matryon-iva cw@^'Cq,UN9#~VW, zhython: a2By=..NC)SN4#7
def register(request):

    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'New account created {user.username}')
            return redirect('/home/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(request,"users/register.html",{"form": form})

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, 'You have logged out.')
    return redirect('/home/')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"You have been logged in")
                return redirect('/home/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = AuthenticationForm()

    return render(request, 'users/login.html',
                  {'form':form})

def user_profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('user profile',user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(request, 'users/user_profile.html', context={'form': form})

    return redirect('home/')


def show_users_recipes(request,id):
    recipes_by_author = Recipe.objects.filter(recipe_author=id)
    return render(request, 'users/authors_recipes.html',
                  {'recipes_by_author':recipes_by_author})
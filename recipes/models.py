from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField, IntegerField
from django.utils import timezone

from users.models import CustomUser


class Recipe(models.Model):
    DISHES_CATEGORY = {
        'first dish': {
            'soup': 'soup',
            'broth': 'broth',
            'chowder': 'chowder',
            'other': 'other'
        },

        'second dish': {
            'porridge': 'porridge',
            'meat dish': 'meat dish',
            'fish dish': 'fish dish',
            'salad': 'salad',
            'other': 'other',


        },

        'desserts': {
            'cake': 'cake',
            'tart': 'tart',
            'muffin': 'muffin',
            'ice-cream': 'ice-cream',
            'milk': 'milk',
            'other': 'other',

        },
        'beverages': {
            'tea': 'tea',
            'cacao': 'cacao',
            'coffe': 'coffee',
            'cocktail': 'cocktail',
            'juice': 'juice',
            'other': 'other'
        },
    }

    COOK_LEVELS = {
        'E': 'Simple',
        'A': 'Average',
        'C': 'Complex',
    }

    objects = None
    recipe_author = models.ForeignKey(get_user_model(),
                                      on_delete=models.CASCADE)
    recipe_title = models.CharField(max_length=25,
                                    default='a delicious recipe')
    dish_type = models.CharField(max_length=30, choices=DISHES_CATEGORY,
                                 default='dish type')
    cooking_level = models.CharField(max_length=1, choices=COOK_LEVELS,
                                     default='simple')
    portion_qty = models.IntegerField(verbose_name="Serving",
                                      default=1)
    cooking_time = (models.IntegerField
                    (help_text='Enter cooking time in minutes', default=10))
    ingredients = (models.TextField
                   (max_length=500, default='for example, oranges, 1, kg',
                    help_text='Enter ingredient, quantity and units'))
    directions = (models.TextField
                  (max_length=2000, default='first step is ...'))
    taste = (models.CharField
             (max_length=170, default='spicy',
              blank=True, help_text='Describe taste'))
    date_published = (models.DateTimeField
                      ('Date published', default=timezone.now))
    date_modified = (models.DateTimeField
                     ('Date edited', default=timezone.now))
    # recipe_slug = models.SlugField('Recipe slug', unique=True)
    image = models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return (f'{self.recipe_author}, {self.recipe_title},'
                f' {self.dish_type}, {self.portion_qty},\
        {self.cooking_level}, {self.ingredients}, {self.directions},\
        {self.taste}, {self.image}')

    class Meta:
        verbose_name_plural = 'Recipe'

    def ingredients_summary(self):
        few_ingredients = self.ingredients.split()
        return f'{" ".join(few_ingredients[:10])}...'

    def description_summary(self):
        brief_desc = self.directions.split()
        return f'{" ".join(brief_desc[:15])}...'


class RecipeCategory(models.Model):

    dish_type = models.ManyToManyField(Recipe)

    def __str__(self):
        return f'{self.dish_type}'


class RecipeInfo(models.Model):
    dish_type = models.ForeignKey(RecipeCategory,
                                  on_delete=models.CASCADE)
    recipe_title = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    recipe_author = models.ForeignKey(get_user_model(),
                                      default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return f'{self.recipe_author},{self.dish_type}, {self.recipe_title}'

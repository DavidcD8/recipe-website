from celery import shared_task
from .models import Recipe
from django.db.models import Avg


@shared_task
def rotate_featured_recipes():
    # Fetch the top-rated recipes (limit to the top 3 by average rating)
    featured_recipes = Recipe.objects.annotate(
        avg_rating=Avg('rating__value')
    ).order_by('-avg_rating')[:3]

    # Reset the featured flag for all recipes
    Recipe.objects.update(featured=False)

    # Mark the top 3 recipes as featured
    for recipe in featured_recipes:
        recipe.featured = True
        recipe.save()

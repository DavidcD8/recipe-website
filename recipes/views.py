from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Recipe, Rating
from django.core.paginator import Paginator
from django.db.models import Avg
from django.utils import timezone


# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            # Redirect to the recipe list view
            return redirect('recipe_list')  # Use the name of the recipe_list URL
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
    
# Home view
def home(request):
    # Fetch the top-rated recipes (limit to the top 3 by average rating)
    featured_recipes = Recipe.objects.annotate(
        avg_rating=Avg('rating__value')
    ).order_by('-avg_rating')[:3]  # Getting the top 3 recipes by rating

    # Update the `featured` flag for these recipes (Optional: If you want to store it in the DB)
    Recipe.objects.update(featured=False)  # Reset previous featured recipes
    for recipe in featured_recipes:
        recipe.featured = True
        recipe.save()

    all_recipes = Recipe.objects.all()  # Fetch all recipes (you can paginate this)

    return render(request, 'recipes/home.html', {
        'featured_recipes': featured_recipes,
        'all_recipes': all_recipes,
    })
    


# List all recipes
def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')

    paginator = Paginator(recipes, 10)  # Show 10 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_list.html', {'page_obj': page_obj})


# Display recipe details with the rating system
@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    average_rating = recipe.average_rating()  # Get the average rating for the recipe
    user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()  # Check if the user has already rated the recipe

    if request.method == 'POST':
        rating_value = request.POST.get('rating')  # Get the selected rating value from the form

        if rating_value:
            rating_value = int(rating_value)

            # If the user has already rated, update their rating
            if user_rating:
                user_rating.value = rating_value
                user_rating.save()
            else:
                # Otherwise, create a new rating
                Rating.objects.create(recipe=recipe, user=request.user, value=rating_value)

            return redirect('recipe_detail', pk=recipe.pk)  # Redirect to the same recipe page after submitting the rating

    context = {
        'recipe': recipe,
        'average_rating': average_rating,
        'user_rating': user_rating,  # Pass the user's rating to the template
    }

    return render(request, 'recipes/recipe_detail.html', context)

# Add a new recipe
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})



@login_required
def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        value = int(request.POST.get('rating', 0))
        if 1 <= value <= 5:  # Ensure the rating is valid
            Rating.objects.update_or_create(
                user=request.user, recipe=recipe,
                defaults={'value': value}
            )
        return redirect('recipe_detail', pk=recipe.id)
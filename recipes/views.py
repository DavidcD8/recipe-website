# views.py
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from .forms import RecipeForm
from .models import Recipe, Rating
from PIL import Image
from taggit.models import Tag
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from .forms import RecipeForm




def handler404(request, exception):
    return render(request, 'recipes/404.html', status=404)


def tag_filter(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    recipes = Recipe.objects.filter(tags__name=tag_name)
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'tag': tag})



# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('recipe_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



# home view
def home(request):
    # Get all tags for the sidebar filter
    tags = Tag.objects.all().order_by('name')[:10]

    # Featured recipes with highest average ratings
    featured_recipes = Recipe.objects.annotate(
        avg_rating=Avg('rating__value')
    ).order_by('-avg_rating')[:4]

    # Newest recipes (sorted by Recipe's created_at field, limited to 4)
    new_recipes = Recipe.objects.all().order_by('-created_at')[:4]

    # Popular recipes: recipes with average ratings >= 5 over the past 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    popular_recipes = Recipe.objects.filter(
        created_at__gte=thirty_days_ago
    ).annotate(
        avg_rating=Avg('rating__value')
    ).filter(
        avg_rating__gte=5  # Filter recipes with avg_rating >= 5
    ).order_by('-avg_rating')[:5]

    # Range for displaying stars in the template
    ratings_range = range(1, 6)

    context = {
        'featured_recipes': featured_recipes,
        'new_recipes': new_recipes,
        'popular_recipes': popular_recipes,
        'ratings_range': ratings_range,
        'tags': tags,  # Use the fetched tags here
    }

    return render(request, 'recipes/home.html', context)





# Recipe list
def recipe_list(request):
    # Instantiate the form with GET data
    form = RecipeForm(request.GET)

    # Start with all recipes
    recipes = Recipe.objects.all()

    if form.is_valid():  # Check if the form is valid
        q = form.cleaned_data['q']
        difficulty = form.cleaned_data['difficulty']
        category = form.cleaned_data['category']

        # Search by title, ingredients, or instructions
        if q:
            recipes = recipes.filter(
                Q(title__icontains=q) | Q(ingredients__icontains=q) | Q(instructions__icontains=q)
            )

        # Filter by difficulty
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)

        # Filter by category
        if category:
            recipes = recipes.filter(category=category)

    recipes = recipes.order_by('-created_at')

    # Fetch choices for consistency
    difficulties = [choice[0] for choice in Recipe._meta.get_field('difficulty').choices]
    categories = [choice[0] for choice in Recipe._meta.get_field('category').choices]

    # Pagination
    paginator = Paginator(recipes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,  # Pass the form to the template
        'page_obj': page_obj,
        'difficulties': difficulties,
        'categories': categories,
    }

    return render(request, 'recipes/recipe_list.html', context)





# Recipe detail view
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    average_rating = recipe.average_rating()
    user_rating = None

    # Only fetch user_rating if the user is authenticated
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()

    if request.method == 'POST':
        # Ensure the user is authenticated before processing the rating
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect unauthenticated users to the login page

        rating_value = request.POST.get('rating')

        if rating_value:
            rating_value = int(rating_value)

            # Validate rating value (should be between 1 and 5)
            if rating_value < 1 or rating_value > 5:
                return render(request, 'recipes/recipe_detail.html', {
                    'recipe': recipe,
                    'average_rating': average_rating,
                    'user_rating': user_rating,
                    'error': 'Rating must be between 1 and 5.'
                })

            if user_rating:
                user_rating.value = rating_value
                user_rating.save()
            else:
                Rating.objects.create(recipe=recipe, user=request.user, value=rating_value)

            return redirect('recipe_detail', pk=recipe.pk)

    context = {
        'recipe': recipe,
        'average_rating': average_rating,
        'user_rating': user_rating,
    }
    return render(request, 'recipes/recipe_detail.html', context)



# Add recipe view
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            try:
                # Check image dimensions
                img = Image.open(image)
                width, height = img.size
                if width < 1024 or height < 768:
                    raise ValidationError("The image must be at least 1024px wide and 768px tall.")
            except Exception as e:
                form.add_error('image', "The image must be at least 1024px wide and 768px tall.")
                return render(request, 'recipes/add_recipe.html', {'form': form})

            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # Manually add the tags since we're using MultipleChoiceField
            for tag_name in form.cleaned_data['tags']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                recipe.tags.add(tag)

            return redirect('recipe_list')
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})

# Rating view
@login_required
def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        value = int(request.POST.get('rating', 0))

        if 1 <= value <= 5:
            Rating.objects.update_or_create(
                user=request.user, recipe=recipe,
                defaults={'value': value}
            )
        else:
            # Redirect with an error message if rating is out of range
            return redirect('recipe_detail', pk=recipe.id)

    return redirect('recipe_detail', pk=recipe.id)
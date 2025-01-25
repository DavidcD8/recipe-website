# views.py
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

# Home view
def home(request):
    # Get all tags for the sidebar filter
    tags = Tag.objects.all().order_by('name')[:10]  # Fetch tags

    # Featured recipes with highest average ratings
    featured_recipes = Recipe.objects.annotate(
        avg_rating=Avg('rating__value')
    ).order_by('-avg_rating')[:3]

    # Newest recipes
    new_recipes = Recipe.objects.all().order_by('-created_at')[:5]

    # Suggested recipes, assuming these are based on highest ratings again
    suggested_recipes = Recipe.objects.annotate(
        avg_rating=Avg('rating__value')
    ).order_by('-avg_rating')[:5]

    # Range for displaying stars in the template
    ratings_range = range(1, 6)

    # Pass the tags to the template for the sidebar
    context = {
        'featured_recipes': featured_recipes,
        'new_recipes': new_recipes,
        'all_recipes': Recipe.objects.all(),  # all recipes for potential further use
        'suggested_recipes': suggested_recipes,
        'ratings_range': ratings_range,
        'tags': tags,  # Use the fetched tags here, not TAGS
    }

    return render(request, 'recipes/home.html', context)

# Recipe list view
def recipe_list(request):
    q = request.GET.get('q', '')
    difficulty = request.GET.get('difficulty', '')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')

    recipes = Recipe.objects.all()

    if q:
        recipes = recipes.filter(Q(title__icontains=q) | Q(ingredients__icontains=q) | Q(instructions__icontains=q))
    
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    
    if category:
        recipes = recipes.filter(category=category)

    if tag:
        recipes = recipes.filter(tags__name__icontains=tag)

    recipes = recipes.order_by('-created_at')
    
    paginator = Paginator(recipes, 10) # Show 10 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_list.html', {'page_obj': page_obj})


# Recipe detail view
@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    average_rating = recipe.average_rating()
    user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()

    if request.method == 'POST':
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

# Add recipe view@login_required
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
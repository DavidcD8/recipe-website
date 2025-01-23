from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating value from 1 to 5

    def __str__(self):
        return f"Rating for {self.recipe.title} by {self.user.username}: {self.value}"



class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/images/', blank=False, null=False)
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField()
    difficulty = models.CharField(
        max_length=10,
        choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('Appetizer', 'Appetizer'),
            ('Main Course', 'Main Course'),
            ('Dessert', 'Dessert'),
            ('Snack', 'Snack'),
            ('Drink', 'Drink'),
        ],
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)


    def average_rating(self):
        # Calculate the average rating for the recipe
        ratings = Rating.objects.filter(recipe=self)
        if ratings.exists():
            return round(sum([rating.value for rating in ratings]) / ratings.count(), 1)  # Ensure it's a float with 1 decimal place
        return 0  # No ratings yet

    def __str__(self):
        return self.title
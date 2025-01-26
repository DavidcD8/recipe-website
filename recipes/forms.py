from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    TAGS_CHOICES = (
    ('Vegetarian', 'Vegetarian'),
    ('Low Carb', 'Low Carb'),
    ('Gluten-Free', 'Gluten-Free'),
    ('Dessert', 'Dessert'),
    ('Quick', 'Quick'),
    ('Healthy', 'Healthy'),
    ('Vegan', 'Vegan'),
    ('Spicy', 'Spicy'),
    ('Comfort Food', 'Comfort Food'),
    ('High Protein', 'High Protein'),
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Snack', 'Snack'),
    ('Keto', 'Keto'),
    ('Paleo', 'Paleo'),
    ('Holiday', 'Holiday'),
    ('Family-Friendly', 'Family-Friendly'),
    ('Mediterranean', 'Mediterranean'),
    ('Asian', 'Asian'),
    ('Italian', 'Italian'),
    ('Caribbean', 'Caribbean'),
    ('Tropical', 'Tropical'),
    ('Seafood', 'Seafood'),
    ('Plantain', 'Plantain'),
    ('Curry', 'Curry'),
    ('Stews', 'Stews'),
)

    tags = forms.MultipleChoiceField(
        choices=TAGS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False  # Tags are not mandatory
    )

    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'image', 'prep_time', 'cook_time', 'servings', 'difficulty', 'category', 'tags']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        # If you want to customize the widget for tags further:
        self.fields['tags'].widget.attrs.update({'class': 'checkbox-tags'})
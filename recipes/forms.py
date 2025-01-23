from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'ingredients', 'instructions', 'image', 
            'prep_time', 'cook_time', 'servings', 'difficulty', 
            'category'
        ]
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter ingredients, one per line'}),
            'instructions': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter instructions, one per line'}),
        }
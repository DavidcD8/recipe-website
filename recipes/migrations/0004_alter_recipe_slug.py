# Generated by Django 5.1.5 on 2025-01-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_slug_alter_rating_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]

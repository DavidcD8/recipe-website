
# Easy Recipe

A web platform to share, browse, and rate delicious recipes. Users can submit their own recipes, view detailed recipe information, and rate others' recipes.

## Features

- **Browse Featured Recipes**: A curated section of featured recipes displayed in grid format.
- **View Recipe Details**: Users can view detailed information about a recipe, including ingredients, preparation steps, and ratings.
- **Rate Recipes**: Users can rate recipes they have tried, with average ratings displayed.
- **Add New Recipes**: Users can submit their own recipes, including images, ingredients, instructions, and ratings.

## Installation

To set up the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/recipe-website.git
   cd recipe-website
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser to access the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the website at `http://127.0.0.1:8000/`.

## Usage

- **Home Page**: Display a hero section and featured recipes.
- **Recipe Details**: Clicking on a recipe will show detailed information including ingredients, instructions, ratings, and a form to submit ratings.
- **Add Recipe**: A form allows users to add new recipes, including uploading images and entering ingredients and preparation instructions.

## Bugs and Fixes

### Bug 1: Recipe Rating Display
**Issue**: The recipe ratings display a numeric average, but it was previously hard to display the star ratings alongside it.


**Fix**: The star ratings were not being rendered properly, which caused issues with displaying the rating stars alongside the numeric value. The fix involved looping through the values 1 to 5 and comparing them with the average rating value, ensuring that the stars are correctly displayed and aligned with the numeric rating.
   - The star ratings are now properly rendered based on the average rating, allowing users to see both the visual representation (stars) and the numeric rating.
   - Example: If the average rating is 4.5, the stars will show four filled stars (★) and one empty star (☆).


### Bug 2: Missing Recipe Image Handling
**Issue**: Some recipes did not have images, resulting in broken image links or a blank space.

**Fix**: A fallback image is displayed if the recipe does not have an associated image. This is done by checking whether the recipe has an image and using a placeholder image if not.

### Bug 3: Layout Issues with Recipe Grid
**Issue**: On mobile devices, the recipe grid was not responsive, and the cards did not adjust properly.

**Fix**: The layout of the recipe grid was improved using CSS grid to ensure it is responsive. The grid now adjusts to the available space and ensures that cards appear neatly on all screen sizes.

### Bug 4: Inconsistent Recipe Submission
**Issue**: When adding new recipes, there was no validation to check if required fields (e.g., title, ingredients) were filled out.

**Fix**: A form validation has been added to ensure that all required fields are provided before submission. If any field is missing, an error message will be shown.

## Acknowledgements 

This project is developed specifically as a **practice project** to enhance web development skills, especially in Django and front-end frameworks. It's an excellent starting point for anyone looking to build real-world applications while learning!

Enjoy coding and learning with this recipe-sharing platform! 🍳🍲🍰

## Project Inspiration 
- This project was inspired by a previous design I created in Figma for another web application. The visual layout and design elements, such as the recipe grid and rating system, were adapted from that design to create a clean and user-friendly experience for browsing and rating recipes.

 
import requests
import json

class Generator:
    def __init__(self, nutrition_input: list, diet_preference: str, ingredients: list = [], params: dict = {'n_neighbors': 5, 'return_distance': False}):
        self.nutrition_input = nutrition_input
        self.diet_preference = diet_preference
        self.ingredients = ingredients
        self.params = params

    def set_request(self, nutrition_input: list, diet_preference: str, ingredients: list, params: dict):
        self.nutrition_input = nutrition_input
        self.diet_preference = diet_preference
        self.ingredients = ingredients
        self.params = params

    def filter_recipes_by_diet(self, recipes):
        non_veg_keywords = ['meat', 'fish', 'egg', 'beef', 'chicken', 'pork', 'cod']
        filtered_recipes = []
        
        for recipe in recipes:
            is_non_veg = any(keyword in ' '.join(recipe['RecipeIngredientParts']).lower() for keyword in non_veg_keywords)
            
            if self.diet_preference == 'Vegetarian' and not is_non_veg:
                filtered_recipes.append(recipe)
            elif self.diet_preference == 'Non Vegetarian' and is_non_veg:
                filtered_recipes.append(recipe)
        
        return filtered_recipes

    def generate(self):
        request = {
            'nutrition_input': self.nutrition_input,
            'ingredients': self.ingredients,
            'params': self.params
        }
        response = requests.post(url='http://localhost:8080/predict/', data=json.dumps(request))
        recipes = response.json()['output']

        filtered_recipes = self.filter_recipes_by_diet(recipes)
        return filtered_recipes

import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php"

def fetch_recipes_mealdb(meal_name):
    """Fetch detailed recipes from TheMealDB API."""
    try:
        print(f"🔍 Fetching recipes for: {meal_name}")

        response = requests.get(BASE_URL, params={"s": meal_name})
        response.raise_for_status()
        data = response.json()

        # Print raw API response before processing
        print("\n📥 Raw API Response:", data, flush=True)

        if not data.get("meals"):
            print("⚠️ No recipes found.")
            return []

        detailed_recipes = []
        for meal in data["meals"]:
            ingredients = [
                meal[f"strIngredient{i}"] for i in range(1, 21)
                if meal[f"strIngredient{i}"]
            ]

            recipe = {
                "id": meal.get("idMeal", ""),
                "title": meal.get("strMeal", ""),
                "category": meal.get("strCategory", ""),
                "instructions": meal.get("strInstructions", ""),
                "image": meal.get("strMealThumb", ""),
                "ingredients": ingredients,
                "source_url": meal.get("strSource", ""),
                "youtube_url": meal.get("strYoutube", ""),
            }

            detailed_recipes.append(recipe)

        return detailed_recipes

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return []

# if __name__ == "__main__":
#     meal_name = input("Enter meal name: ").strip()
#     recipes = fetch_recipes_mealdb(meal_name)
#
#     if recipes:
#         print("\n🍽️ Recipe Details:\n")
#         for recipe in recipes:
#             print(f"📌 Title: {recipe['title']}")
#             print(f"📺 YouTube Video: {recipe['youtube_url'] or '🚫 No video available'}")
#             print("-" * 40)
#     else:
#         print("⚠️ No recipes found.")

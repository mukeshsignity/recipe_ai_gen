import requests

EDAMAM_APP_ID = "c9b28b0f"
EDAMAM_API_KEY = "ff1ccd42a9ef6279579acc74460ac79a"
EDAMAM_URL = "https://api.edamam.com/search"

DEFAULT_VIDEO_URL = "https://www.youtube.com/results?search_query=how+to+cook"  # Fallback link


def fetch_recipes_edamam(ingredients):
    """Fetch detailed recipes from Edamam API, ensuring similar functionality to Spoonacular."""
    if not EDAMAM_APP_ID or not EDAMAM_API_KEY:
        raise ValueError("❌ Missing Edamam API credentials. Set APP_ID and API_KEY.")

    params = {
        "q": ",".join(ingredients),
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_API_KEY,
        "from": 0,
        "to": 5,  # Fetch 5 recipes
    }

    try:
        print(f"🔍 Fetching recipes with ingredients: {ingredients}")  # Debugging
        response = requests.get(EDAMAM_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Print full response to debug
        print(f"📝 Edamam API Response: {data}")

        if "hits" not in data or not data["hits"]:
            print("⚠️ No recipes found.")
            return []

        detailed_recipes = []

        for hit in data["hits"]:
            recipe = hit["recipe"]

            # Fetch video link
            video_url = fetch_video_link(recipe["label"])

            # Structure response to match Spoonacular's output
            detailed_recipes.append({
                "id": recipe["uri"].split("_")[-1],  # Extract recipe ID from URI
                "title": recipe["label"],
                "ingredients": recipe["ingredientLines"],
                "instructions": recipe.get("url", "No instructions provided."),  # Edamam lacks direct instructions
                "image": recipe.get("image", ""),
                "servings": recipe.get("yield", "N/A"),
                "prep_time": "N/A",  # Edamam doesn’t provide prep time
                "source_url": recipe.get("url", ""),
                "video_url": video_url  # Added video link
            })

        print(f"✅ Found {len(detailed_recipes)} recipes")  # Debugging
        return detailed_recipes

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return []


def fetch_video_link(recipe_title):
    """Fetch a relevant cooking video link from YouTube."""
    search_query = recipe_title.replace(" ", "+") + "+recipe"
    youtube_search_url = f"https://www.youtube.com/results?search_query={search_query}"

    return youtube_search_url if recipe_title else DEFAULT_VIDEO_URL

import requests

# Spoonacular API Key
SPOONACULAR_API_KEY = "818ada7831fc400ea73483e42b0d63d0"

# YouTube API Key (For testing, replace with your own)
YOUTUBE_API_KEY = "AIzaSyBy1XLpCgMyOokxcKDKZCdHHJn2j_e1GNY"

# API Base URLs
SPOONACULAR_BASE_URL = "https://api.spoonacular.com/recipes"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def fetch_recipes(ingredients):
    if not SPOONACULAR_API_KEY:
        raise ValueError("Missing Spoonacular API Key.")

    find_params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": SPOONACULAR_API_KEY
    }

    try:
        response = requests.get(f"{SPOONACULAR_BASE_URL}/findByIngredients", params=find_params)
        response.raise_for_status()
        recipes = response.json()

        if not recipes:
            return []

        detailed_recipes = []
        for recipe in recipes:
            recipe_id = recipe["id"]
            info_params = {"apiKey": SPOONACULAR_API_KEY, "includeNutrition": False}
            info_response = requests.get(f"{SPOONACULAR_BASE_URL}/{recipe_id}/information", params=info_params)
            info_response.raise_for_status()
            recipe_info = info_response.json()

            # Fetch specific YouTube video
            youtube_video_url = fetch_youtube_video(recipe_info["title"])

            detailed_recipes.append({
                "id": recipe_info["id"],
                "title": recipe_info["title"],
                "ingredients": [ing["original"] for ing in recipe_info["extendedIngredients"]],
                "instructions": recipe_info.get("instructions", "No instructions provided."),
                "image": recipe_info.get("image", ""),
                "servings": recipe_info.get("servings", "N/A"),
                "prep_time": recipe_info.get("readyInMinutes", "N/A"),
                "source_url": recipe_info.get("sourceUrl", ""),
                "youtube_url": youtube_video_url  # Direct video link
            })

        return detailed_recipes
    except requests.exceptions.RequestException as e:
        print("Error fetching recipes:", e)
        return []


def fetch_youtube_video(recipe_title):
    search_query = f"{recipe_title} recipe"
    params = {
        "part": "snippet",
        "q": search_query,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "items" in data and data["items"]:
            video_id = data["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1"  # Direct embeddable video URL

        return None
    except requests.exceptions.RequestException as e:
        print("Error fetching YouTube video:", e)
        return None


# # ✅ Test Example
# if __name__ == "__main__":
#     test_ingredients = ["tomato", "cheese", "basil"]
#     recipes = fetch_recipes(test_ingredients)
#     for r in recipes:
#         print(r["title"], "➡", r["youtube_url"])

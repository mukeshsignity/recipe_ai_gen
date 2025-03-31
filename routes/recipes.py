from fastapi import APIRouter, UploadFile, File, HTTPException
from services.recipe_fetcher import fetch_recipes
from models.ingredient_detector import IngredientDetector

router = APIRouter()
detector = IngredientDetector()


@router.post("/suggest")
async def suggest_recipes(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Invalid file. Please upload an image.")

        detected_ingredients = detector.detect_ingredients(image_bytes)
        if not detected_ingredients:
            raise HTTPException(status_code=400, detail="No ingredients detected. Please upload a valid image.")

        recipes = fetch_recipes(detected_ingredients)
        if not recipes:
            raise HTTPException(status_code=404, detail="No recipes found for detected ingredients.")

        return {"success": True, "ingredients_detected": detected_ingredients, "suggested_recipes": recipes}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# from fastapi import APIRouter, UploadFile, File, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# from backend.services.mealdb_fatch_recipe import fetch_recipes_mealdb
# from backend.services.recipe_fetcher import fetch_recipes
# from backend.models.ingredient_detector import IngredientDetector
#
# router = APIRouter()  # API prefix
# detector = IngredientDetector()
#
# # Response Model
# class Recipe(BaseModel):
#     id: str
#     title: str
#     category: Optional[str] = None
#     area: Optional[str] = None
#     instructions: Optional[str] = None
#     image: Optional[str] = None
#     ingredients: List[str]
#     source_url:Optional[str] = None
#     youtube_url: Optional[str] = None  # Ensure YouTube URL is included
#
# class RecipeResponse(BaseModel):
#     success: bool
#     ingredients_detected: List[str]
#     suggested_recipes: List[Recipe]
#
# @router.post("/suggest", response_model=RecipeResponse, summary="Get recipe suggestions from an image")
# async def suggest_recipes(
#         file: UploadFile = File(...),
#         dietary_preferences: str = ""  # Placeholder for future filtering logic
# ):
#     """
#     Detects ingredients from an uploaded image and fetches relevant recipe suggestions.
#     Uses TheMealDB API for fetching meal-based recipes.
#     """
#     try:
#         # Step 1: Read Image File
#         image_bytes = await file.read()
#         if not image_bytes:
#             raise HTTPException(status_code=400, detail="❌ Invalid file. Please upload an image.")
#
#         # Step 2: Detect Ingredients (using YOLO)
#         detected_ingredients = detector.detect_ingredients(image_bytes)
#         print(f"🔍 Detected Ingredients: {detected_ingredients}")
#
#         if not detected_ingredients:
#             raise HTTPException(status_code=400, detail="❌ No ingredients detected. Please upload a valid image.")
#
#         # Step 3: Use the first detected ingredient as the meal name
#         meal_name = detected_ingredients[0]  # Example: "Chicken", "Egg", etc.
#         recipes = fetch_recipes(meal_name)
#
#         if not recipes:
#             raise HTTPException(status_code=404, detail="❌ No recipes found for detected ingredients.")
#
#         response = RecipeResponse(
#             success=True,
#             ingredients_detected=detected_ingredients,
#             suggested_recipes=recipes,
#         )
#         print(f"📤 Final Response: {response}")
#
#         return response
#
#     except HTTPException as http_err:
#         raise http_err
#
#     except Exception as e:
#         print(f"⚠️ Internal Server Error: {str(e)}")
#         raise HTTPException(status_code=500, detail="⚠️ Internal Server Error.")

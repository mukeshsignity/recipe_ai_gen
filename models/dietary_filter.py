from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.recipe_fetcher import fetch_recipes
from backend.models.ingredient_detector import IngredientDetector

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

from fastapi import APIRouter, UploadFile, File, HTTPException
from models.ingredient_detector import IngredientDetector

router = APIRouter()

# Initialize the ingredient detector without arguments
detector = IngredientDetector()


@router.post("/detect")
async def detect_ingredients(file: UploadFile = File(...)):
    """Detect ingredients from an uploaded image."""
    try:
        image_bytes = await file.read()
        detected_ingredients = detector.detect_ingredients(image_bytes)

        if not detected_ingredients:
            raise HTTPException(status_code=400, detail="No ingredients detected.")

        return {"ingredients": detected_ingredients}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

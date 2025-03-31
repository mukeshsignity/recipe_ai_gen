from fastapi import FastAPI
from routes import ingredients, recipes, cooking_assistant
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="AI Recipe Suggestion System",
    description="API for ingredient detection and recipe recommendation",
    version="1.0.0"
)

# Enable CORS (optional, but useful for frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, update for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(ingredients.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(cooking_assistant.router, prefix="/api")  # Fixed this line

@app.get("/")
def root():
    return {"message": "AI Recipe Suggestion System API"}

# Enable Swagger UI
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")

# Redoc documentation
@app.get("/redoc", include_in_schema=False)
def custom_redoc_ui():
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(openapi_url="/openapi.json", title="API Documentation")



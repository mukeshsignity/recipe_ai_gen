import requests

EDAMAM_APP_ID = "c9b28b0f"
EDAMAM_API_KEY = "ff1ccd42a9ef6279579acc74460ac79a	— "
EDAMAM_URL = "https://api.edamam.com/api/recipes/v2"

def test_edamam_manual():
    params = {
        "type": "public",  # Required for Recipe API v2
        "q": "egg",
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_API_KEY,
        "from": 0,
        "to": 5,
    }

    try:
        response = requests.get(EDAMAM_URL, params=params)
        response.raise_for_status()
        data = response.json()
        print("✅ API Response:", data)

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")

# Run the test
test_edamam_manual()

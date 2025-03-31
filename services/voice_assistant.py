import openai
import os
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_KEY = os.getenv("OPENAI_ORG_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is missing! Ensure .env file is correctly configured.")

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORG_KEY

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)  # Adjust speech rate for clarity

def speak(text: str):
    """Convert text to speech and play it."""
    engine.say(text)
    engine.runAndWait()
    return {"message": "Speech output played successfully"}

import speech_recognition as sr

def listen():
    """Capture voice input and return recognized text."""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for voice input...")
            try:
                audio = recognizer.listen(source, timeout=5)  # Limit wait time
                recognized_text = recognizer.recognize_google(audio, language="en-US")
                return {"text": recognized_text}
            except sr.UnknownValueError:
                return {"error": "Speech not understood"}
            except sr.RequestError:
                return {"error": "Speech recognition service unavailable"}
            except TimeoutError:  # Corrected from `sr.WaitTimeoutError`
                return {"error": "No speech detected, try again"}
    
    except OSError:
        return {"error": "No microphone detected. Please check your device."}


def generate_ai_response(user_input: str):
    """Generate AI response based on user input, responding to greetings and enforcing cooking-related topics."""
    try:
        # System prompt ensuring the AI stays within the cooking and meal planning domain
        system_prompt = (
            "You are an AI Cooking Assistant. Provide detailed, structured, and well-explained responses "
            "only related to cooking, recipes, meal planning, ingredient substitutions, and food-related topics. "
            "Do NOT respond to any queries unrelated to these topics. Ensure responses are well-structured, "
            "informative, and detailed, presented in clear paragraph format."
        )

        # Greeting detection
        greeting_keywords = [
            "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"
        ]
        cooking_keywords = [
            "recipe", "meal", "cook", "cooking", "ingredient", "food", "dish", "baking",
            "grilling", "boiling", "roasting", "spices", "flavor", "substitutions", "nutrition",
            "healthy eating", "meal prep", "kitchen", "grocery", "diet", "calories"
        ]

        # Respond to greetings separately
        if any(word in user_input.lower() for word in greeting_keywords):
            return {"response": "Hello! How can I assist you with cooking, recipes, or meal planning today?"}

        # Check if the input is related to cooking
        if not any(word in user_input.lower() for word in cooking_keywords):
            return {
                "response": "I can only assist with cooking, recipes, and meal planning. "
                            "Please ask about meal preparation, ingredient substitutions, or food-related topics."
            }

        # AI response generation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )

        ai_reply = response["choices"][0]["message"]["content"]
        return {"response": ai_reply}

    except openai.error.OpenAIError as e:
        return {"error": f"OpenAI API Error: {str(e)}"}


def listen_and_respond():
    """Capture voice input, process it, generate AI response, and speak the response."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("Listening for voice command...")
            audio = recognizer.listen(source, timeout=5)
            recognized_text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {recognized_text}")

            # Generate AI response
            ai_response = generate_ai_response(recognized_text)
            response_text = ai_response.get("response", "Sorry, I couldn't process that.")

            # Speak the response
            speak(response_text)

            return {"user_input": recognized_text, "ai_response": response_text}

        except sr.UnknownValueError:
            return {"error": "Could not understand the audio"}
        except sr.RequestError:
            return {"error": "Speech Recognition API request failed"}
        except sr.WaitTimeoutError:
            return {"error": "No speech detected, try again"}

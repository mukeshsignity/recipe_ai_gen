from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import speech_recognition as sr
import os
from services.voice_assistant import generate_ai_response, speak, listen, listen_and_respond

router = APIRouter()

class ChatQuery(BaseModel):
    message: str

@router.post("/chat/")
async def ai_chat(query: ChatQuery):
    """Text-based AI chat endpoint"""
    response = generate_ai_response(query.message)
    return JSONResponse(content=response)

@router.post("/speak/")
async def ai_speak(query: ChatQuery):
    """Convert text to speech"""
    response = speak(query.message)
    return JSONResponse(content=response)

@router.get("/listen/")
async def ai_listen():
    """Listen for live voice input and return recognized text"""
    response = listen()
    return response

@router.get("/listen-and-respond/")
async def ai_direct_voice_command():
    """Process real-time voice input, generate AI response, and speak it"""
    response = listen_and_respond()
    return JSONResponse(content=response)

# @router.post("/voice-command/upload/")
# async def ai_voice_command(audio: UploadFile = File(...)):
#     """Process uploaded audio file, recognize speech, and return AI response"""
#     recognizer = sr.Recognizer()
#     temp_audio_path = "temp_audio.wav"
#
#     try:
#         # Save uploaded file temporarily
#         with open(temp_audio_path, "wb") as buffer:
#             buffer.write(audio.file.read())
#
#         with sr.AudioFile(temp_audio_path) as source:
#             recognizer.adjust_for_ambient_noise(source)
#             audio_data = recognizer.record(source)
#             recognized_text = recognizer.recognize_google(audio_data)
#
#             # Generate AI response
#             response = generate_ai_response(recognized_text)
#
#         # Remove temp file after processing
#         os.remove(temp_audio_path)
#
#         return JSONResponse(content={"recognized_text": recognized_text, "ai_response": response})
#
#     except sr.UnknownValueError:
#         return JSONResponse(content={"error": "Could not understand the audio"}, status_code=400)
#     except sr.RequestError:
#         return JSONResponse(content={"error": "Speech Recognition API request failed"}, status_code=503)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
#     finally:
#         # Ensure temp file is deleted even if an exception occurs
#         if os.path.exists(temp_audio_path):
#             os.remove(temp_audio_path)

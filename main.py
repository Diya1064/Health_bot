from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = FastAPI()

# Allow frontend requests (like from your Flutter app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase (assumes you have uploaded a serviceAccountKey.json file)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.get("/")
def read_root():
    return {"message": "Chatbot backend is running successfully!"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_id = body.get("user_id")
    message = body.get("message")

    # Here you'd integrate with your AI logic (Gemini, etc.)
    response = f"Echo: {message}"  # Dummy response for now

    # Store chat history in Firestore
    chat_doc = {
        "user_id": user_id,
        "message": message,
        "response": response
    }
    db.collection("chat_history").add(chat_doc)

    return {"response": response}

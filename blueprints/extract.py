from flask import Blueprint, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
import google.generativeai as genai 

load_dotenv()

extract_bp = Blueprint('extract', __name__, static_folder='static', template_folder='templates')
extract_bp.secret_key = "phaethon"  # Set a secure key for session management

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# System prompt to guide chatbot behavior
system_prompt = os.getenv("SYSTEM_PROMPT")


@extract_bp.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@extract_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Initialize conversation history if not present
    if "conversation" not in session:
        session["conversation"] = [{"role": "user", "parts": [{"text": system_prompt}]}]  # Use user role for system prompt

    # Append user input to conversation history
    session["conversation"].append({"role": "user", "parts": [{"text": user_message}]})

    # Generate response based on the current conversation history
    response = model.generate_content(session["conversation"])
    bot_response = response.text

    # Append model response to session history
    session["conversation"].append({"role": "model", "parts": [{"text": bot_response}]})

    # Limit conversation history to the last 10 exchanges to optimize memory usage
    session["conversation"] = session["conversation"][-10:]

    return jsonify({"response": bot_response})



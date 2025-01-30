from flask import Blueprint, render_template, request, jsonify, session
import google.generativeai as genai 

extract = Blueprint('extract', __name__, static_folder='static', template_folder='templates')
extract.secret_key = "phaethon"  # Set a secure key for session management

# Configure Gemini API
genai.configure(api_key="AIzaSyB0sM7VfxgPEqRYE488fZ2UvJp4Psdv0aI")
model = genai.GenerativeModel("gemini-1.5-flash")

# System prompt to guide chatbot behavior
system_prompt = """You are Iko, an expert in electronic waste dismantling.
Your role is to provide step-by-step guidance on safely disassembling and recycling e-waste.
Prioritize safety measures and explain dismantling procedures clearly. You are friendly and helpful."""

@extract.route('/extract')
def upload():
    return render_template('extract.html')

@extract.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@extract.route("/chat", methods=["POST"])
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



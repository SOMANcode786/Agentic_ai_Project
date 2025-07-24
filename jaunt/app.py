from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI  # Make sure you're using sync version

# Load .env variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Setup OpenAI client (sync)
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta"  # Gemini-compatible base
)

# Flask app
app = Flask(__name__)

# Home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("input", "").strip()
    if not user_input:
        return jsonify({"reply": "Please enter a message."})

    try:
        # Use Gemini (or GPT) completion
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": """
You are a helpful assistant for Jaunt Solutions.

Company: Jaunt Solutions
Slogans:
- Transforming Visions into Digital Reality
- Empowering Businesses For Sustainable Growth

Services:
- ERP Consultancy
- Team Augmentation
- Process Outsourcing
- Business Support & IT Maintenance
- Domain & Email Management
- Software & Mobile App Development
- Website Development
- Digital & Social Media Marketing

Respond professionally and helpfully.
                """},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"reply": f"Something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)  

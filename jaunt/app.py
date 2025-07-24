from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
<<<<<<< HEAD
<<<<<<< HEAD
import asyncio
from agents import OpenAIChatCompletionsModel, Agent, RunConfig, Runner, AsyncOpenAI
=======
from openai import OpenAI  # Make sure you're using sync version
>>>>>>> 38352b44189e505ef55b8cb247d666451cdd0914
=======
from openai import OpenAI  # Make sure you're using sync version
>>>>>>> 38352b44189e505ef55b8cb247d666451cdd0914

# Load .env variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

<<<<<<< HEAD
<<<<<<< HEAD
# Setup Gemini Client
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# Define the model
model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash"
)

with open("jaunt_instructions.txt", "r") as file:
    instructions_text = file.read()

# Create the agent
agent = Agent(
    name="Jaunt Solution agent",
    instructions=instructions_text
)

# Configuration
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# Initialize Flask
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("input", "")
    if not user_input.strip():
        return jsonify({"reply": ""})

    # Read instructions from file
    with open("jaunt_instructions.txt", "r", encoding="utf-8") as file:
        instructions_text = file.read()

    # Create agent (optional: if not created earlier globally)
    agent = Agent(
        name="Jaunt Solution agent",
        instructions=instructions_text
    )

    async def run_agent():
        run = await Runner.run(agent, user_input, run_config=config)
        return run.final_output

    try:
        result = asyncio.run(run_agent())

        # ✅ Store chat history in new file
        with open("chat_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"User: {user_input}\n")
            log_file.write(f"Bot: {result}\n\n")

        return jsonify({"reply": result})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": f"Something went wrong: {str(e)}"})


if __name__ == "__main__":
    app.run(port=4000, debug=True)
=======
=======
>>>>>>> 38352b44189e505ef55b8cb247d666451cdd0914
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
<<<<<<< HEAD
>>>>>>> 38352b44189e505ef55b8cb247d666451cdd0914
=======
>>>>>>> 38352b44189e505ef55b8cb247d666451cdd0914

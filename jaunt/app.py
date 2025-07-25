from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import asyncio

# Agentic-AI dependencies
from agents import OpenAIChatCompletionsModel, Agent, RunConfig, Runner, AsyncOpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Setup Async Gemini client
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# Define the model
model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash"
)

# Load instructions
with open("jaunt_instructions.txt", "r", encoding="utf-8") as file:
    instructions_text = file.read()

# Create agent
agent = Agent(
    name="Jaunt Solution agent",
    instructions=instructions_text
)

# Run config
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# Flask app
app = Flask(__name__)

# Home route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # templates/index.html must exist

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("input", "").strip()
    if not user_input:
        return jsonify({"reply": "Please enter a message."})

    async def run_agent():
        run = await Runner.run(agent, user_input, run_config=config)
        return run.final_output

    try:
        result = asyncio.run(run_agent())

        # Save chat log
        with open("chat_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"User: {user_input}\n")
            log_file.write(f"Bot: {result}\n\n")

        return jsonify({"reply": result})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"reply": f"Something went wrong: {str(e)}"}), 500

# Run the server
if __name__ == "__main__":
    app.run(debug=True, port=4000)

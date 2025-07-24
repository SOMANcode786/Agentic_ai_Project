import chainlit as cl
from agents import Agent, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure AsyncOpenAI client for Gemini
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Create model instance
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

# Define run configuration
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Define your agent
agent = Agent(
    instructions="You are a helpful assistant. Your task is to answer questions related to development.",
    name="Developer_assistant"
)

@cl.on_message
async def handle_chat_message():
    cl.user_session.set("history",[])
    await cl.Message(content="hellow ! i am the development support agent       ")
    

# Handle incoming Chainlit messages
@cl.on_message
async def handle_message(message: cl.Message):
    history=cl.user_session.get("history")
    result = await Runner.run(
        agent,
        input=message.content,
        run_config=config
    )
    
    # Return the message properly
    return await cl.Message(content=result.final_output).send()

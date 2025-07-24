import asyncio
from agents import Agent,Runner

from model_config import config


async def main():
    agent=Agent(
    name="Agent",
    instructions="you are a helful agent you're task i that the user ask a question realted to islam you given answer otherwise user ask other type of question the not relate with islam you send  a message please ask a relevant question "
    )

    input_value=input("Enter your question related to Islam : ")
    result= Runner.run_streamed(
    agent,
    input_value,
    run_config=config,

   )
    
    print(result)

asyncio.run(main())




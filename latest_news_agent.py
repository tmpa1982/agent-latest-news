import logging

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

class LatestNewsAgent:
    endpoint = "https://tmpa-ai-foundry.services.ai.azure.com/models"

    def __init__(self, api_key: str, model_name: str, tools):
        llm = init_chat_model(
            endpoint=self.endpoint,
            model=model_name,
            model_provider="azure_ai",
            credential=api_key,
        )

        self.agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt="You are a member of a team writing jokes for a comedy show. Your responsibility is to curate news headlines that the joke writers can use for the setup.",
        )

    async def invoke(self, message: str) -> str:
        logging.info(f"Invoking LatestNewsAgent with message: {message}")
        response = await self.agent.ainvoke({
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        })
        result = response["messages"][-1].content
        logging.info(f"LatestNewsAgent response: {result}")
        return result

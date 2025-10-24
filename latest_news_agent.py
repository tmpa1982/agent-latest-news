import asyncio
from functools import partial
import json
import logging
from openai import OpenAI

class LatestNewsAgent:
    endpoint = "https://tmpa-ai-foundry.services.ai.azure.com/openai/v1/"

    def __init__(self, api_key: str, model_name: str, tools, tools_invoker):
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=api_key,
        )
        self.model_name = model_name
        self.tools = tools
        self.tools_invoker = tools_invoker

    async def invoke(self, message: str) -> str:
        response = await self.__call_model([
            {
                "role": "user",
                "content": message,
            }
        ])
        return response

    async def __call_model(self, messages):
        logging.info(f"Calling model {self.model_name} with messages: {messages}")
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=self.tools,
        )

        model_message = completion.choices[0].message
        all_messages = messages + [model_message]
        if model_message.tool_calls:
            return await self.__handle_tool_calls(all_messages, model_message.tool_calls)

        return completion.choices[0].message.content

    async def __handle_tool_calls(self, previous_messages, tool_calls):
        messages = previous_messages.copy()
        for tool_call in tool_calls:
            result = await self.__handle_tool_call(tool_call)
            message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(message)
        return await self.__call_model(messages)

    async def __handle_tool_call(self, tool_call) -> any:
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments or "{}")

        if asyncio.iscoroutinefunction(self.tools_invoker):
            return await self.tools_invoker(tool_name, **args)
        else:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                None,
                partial(self.tools_invoker, tool_name, **args)
            )

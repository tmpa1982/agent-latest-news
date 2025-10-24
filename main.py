import asyncio
import logging
import os
from dotenv import load_dotenv
import uvicorn

from a2a_module import A2AModule
from latest_news_agent import LatestNewsAgent
from mcp_module import MCPModule
from tools import LLMTools

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

async def main():
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the AZURE_OPENAI_API_KEY environment variable.")
    model_name = "gpt-5-mini"

    server_script_path="../mcp-news/main.py"
    hostname = "localhost"
    port = 8081
    mcp = MCPModule(
        server_script_path=server_script_path
    )
    await mcp.connect()
    tools = LLMTools()
    a2a = A2AModule(
        host=hostname,
        port=port,
        agent=LatestNewsAgent(api_key, model_name, mcp.get_openai_tools(), mcp.call_tool),
    )

    config = uvicorn.Config(app=a2a.get_starlette(), host=hostname, port=port, loop="asyncio")
    server = uvicorn.Server(config)
    try:
        await server.serve()
    finally:
        await mcp.close()

if __name__ == "__main__":
    asyncio.run(main())

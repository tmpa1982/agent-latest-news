import logging
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPModule:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        params = StdioServerParameters(
            command="python",
            args=[self.server_script_path],
        )
        logging.info(f"Connecting to MCP server with params: {params}")
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(params))
        stdio, write = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()
        tools = await session.list_tools()
        logging.info(f"Connected to MCP server with tools: {tools}")

    async def close(self):
        await self.exit_stack.aclose()

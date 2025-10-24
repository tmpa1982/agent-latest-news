import asyncio
import logging
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPModule:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.exit_stack = AsyncExitStack()

    def get_openai_tools(self):
        openai_tools = []
        for t in self.tools.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description or t.title or f"MCP tool {t.name}",
                    "parameters": t.inputSchema or {"type": "object", "properties": {}},
                },
            })
        return openai_tools

    async def call_tool(self, tool_name: str, **kwargs):
        logging.info(f"Calling MCP tool {tool_name} with args: {kwargs}")
        if not self.session:
            raise ValueError("MCPModule is not connected. Call sync_connect() first.")
        tool = next((t for t in self.tools.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        tool_response = await self.session.call_tool(tool.name, kwargs)
        logging.info(f"Tool {tool_name} response: {tool_response}")
        return tool_response.model_dump_json()

    async def connect(self):
        params = StdioServerParameters(
            command="python",
            args=[self.server_script_path],
        )
        logging.info(f"Connecting to MCP server with params: {params}")
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(params))
        stdio, write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await self.session.initialize()
        self.tools = await self.session.list_tools()
        logging.info(f"Connected to MCP server with tools: {self.tools}")

    async def close(self):
        await self.exit_stack.aclose()
        logging.info("MCPModule connection closed")

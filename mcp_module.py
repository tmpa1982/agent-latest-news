import logging

from langchain_mcp_adapters.client import MultiServerMCPClient  

class MCPModule:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path

    def get_openai_tools(self):
        return self.tools

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
        client = MultiServerMCPClient(
            {
                "math": {
                    "transport": "stdio",
                    "command": "python",
                    "args": [self.server_script_path],
                },
            }
        )

        self.tools = await client.get_tools()
        logging.info(f"Connected to MCP server with tools: {self.tools}")

    async def close(self):
        logging.info("MCPModule connection closed")

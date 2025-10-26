import logging

from langchain_mcp_adapters.client import MultiServerMCPClient  

class MCPModule:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path

    def get_openai_tools(self):
        return self.tools

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

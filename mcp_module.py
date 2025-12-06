import logging
from typing import Any, Dict, List
import io
import sys
from contextlib import redirect_stdout

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import tool

class PythonExecutor:
    def __init__(self, mcp_tools: List[Any]):
        self.mcp_tools = mcp_tools
        self.tool_map = {t.name: t for t in mcp_tools}

    async def execute(self, code: str) -> str:
        """
        Execute Python code that can call MCP tools.
        The tools are available as functions in the global scope.
        """
        local_scope = {}
        
        # We need to map the sanitized names to the actual tools.
        for tool_obj in self.mcp_tools:
            # We want to bind the tool to a name.
            sanitized_name = tool_obj.name.replace("-", "_")
            local_scope[sanitized_name] = tool_obj
            
        # Wrap code in an async function
        indented_code = "\n".join(["    " + line for line in code.splitlines()])
        wrapped_code = f"async def _user_code():\n{indented_code}"
        
        try:
            exec(wrapped_code, local_scope)
            # Find the function and run it
            if "_user_code" in local_scope:
                f = io.StringIO()
                result = None
                with redirect_stdout(f):
                    result = await local_scope["_user_code"]()
                
                output = f.getvalue()
                if result is not None:
                    output += f"\nResult: {result}"
                return output if output else "Code executed successfully."
                
        except Exception as e:
            return f"Error executing code: {e}"
        
        return "No code executed."

class MCPModule:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.executor = None

    def get_openai_tools(self):
        # Return the execute_python tool
        @tool
        async def execute_python(code: str) -> str:
            """
            Execute Python code to interact with tools. 
            Tools are available as global functions (e.g. fetch_news(topic='...')).
            You must await async tool calls. 
            Usage example:
            news = await fetch_news(topic="AI")
            print(news)
            """
            if self.executor:
                return await self.executor.execute(code)
            return "Executor not initialized."
            
        return [execute_python]

    async def connect(self):
        client = MultiServerMCPClient(
            {
                "default": {
                    "transport": "stdio",
                    "command": "python",
                    "args": [self.server_script_path],
                },
            }
        )

        mcp_tools = await client.get_tools()
        self.executor = PythonExecutor(mcp_tools)
        logging.info(f"Connected to MCP server. Tools loaded into executor: {[t.name for t in mcp_tools]}")

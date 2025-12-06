import asyncio
import os
import logging
from dotenv import load_dotenv
from mcp_module import MCPModule
from latest_news_agent import LatestNewsAgent

# Mocking or using real environment?
# The agent relies on Azure OpenAI. We need credentials.
load_dotenv()

logging.basicConfig(level=logging.INFO)

async def verify():
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not api_key:
        print("Skipping verification: No API Key found.")
        return

    # Use the expected server script path
    server_script_path = "../mcp-news/main.py" 
    
    # Check if server script exists
    if not os.path.exists(os.path.join(os.path.dirname(__file__), server_script_path)):
        # Try finding it relative to repo root if needed, or just warn
        print(f"Warning: Server script not found at {server_script_path}. Attempting absolute path resolution.")
        # But we will try to proceed.
    
    mcp = MCPModule(server_script_path)
    await mcp.connect()
    
    tools = mcp.get_openai_tools()
    agent = LatestNewsAgent(api_key, "gpt-5-mini", tools) 

    print("Invoking agent with a request that requires tool usage...")
    try:
        response = await agent.invoke("Find me the latest news about 'Quantum Computing'.")
        print(f"Agent Response: {response}")
        
        if "execute_python" in str(tools):
            print("SUCCESS: execute_python tool is available.")
        else:
            print("FAILURE: execute_python tool missing.")
    except Exception as e:
        import traceback
        with open("error.log", "w") as f:
            f.write(f"FAILURE: Agent invocation failed with error: {e}\n")
            traceback.print_exc(file=f)
        print("FAILURE: Check error.log for details.")

if __name__ == "__main__":
    asyncio.run(verify())

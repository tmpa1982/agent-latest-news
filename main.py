import asyncio
import logging
import uvicorn

from a2a_module import A2AModule
from mcp_module import MCPModule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

async def setupMcp():
    mcp = MCPModule(
        server_script_path="../mcp-news/main.py"
    )
    try:
        await mcp.connect()
    finally:
        await mcp.close()

def main():
    asyncio.run(setupMcp())
    hostname = "localhost"
    port = 8081
    a2a = A2AModule(host=hostname, port=port)
    uvicorn.run(a2a.get_starlette(), port=port)

if __name__ == "__main__":
    main()

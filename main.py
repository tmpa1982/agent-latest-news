import logging
import uvicorn

from a2a_module import A2AModule
from latest_news_agent import LatestNewsAgent
from mcp_module import MCPModule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def main():
    server_script_path="../mcp-news/main.py"
    hostname = "localhost"
    port = 8081
    mcp = MCPModule(
        server_script_path=server_script_path
    )
    mcp.sync_connect()
    a2a = A2AModule(
        host=hostname,
        port=port,
        agent=LatestNewsAgent(),
    )
    uvicorn.run(a2a.get_starlette(), port=port)

if __name__ == "__main__":
    main()

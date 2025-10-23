import socket
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.types import (
    AgentCapabilities,
    AgentCard,
)

def main():
    hostname = socket.gethostname()
    port = 8081
    agent_card = AgentCard(
        name="Latest News Agent",
        description="An agent that provides the latest news updates.",
        url=f"http://${hostname}:{port}",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(),
        skills=[],
    )
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=None,
    )
    uvicorn.run(app.build(), port=port)

if __name__ == "__main__":
    main()

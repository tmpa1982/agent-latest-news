import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.types import (
    AgentCapabilities,
    AgentCard,
)

def main():
    agent_card = AgentCard(
        name="Latest News Agent",
        description="An agent that provides the latest news updates.",
        url="http://localhost:8081",
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
    uvicorn.run(app.build(), port=8081)

if __name__ == "__main__":
    main()

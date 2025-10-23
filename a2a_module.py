from a2a.server.apps import A2AStarletteApplication
from a2a.types import (
    AgentCapabilities,
    AgentCard,
)

class A2AModule:
    def __init__(self, host: str, port: int):
        agent_card = AgentCard(
            name="Latest News Agent",
            description="An agent that provides the latest news updates.",
            url=f"http://${host}:{port}",
            version="1.0.0",
            default_input_modes=["text"],
            default_output_modes=["text"],
            capabilities=AgentCapabilities(),
            skills=[],
        )
        self.app = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=None,
        )

    def get_starlette(self):
        return self.app.build()
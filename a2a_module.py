from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from agent_executor import LatestNewsAgentExecutor
from latest_news_agent import LatestNewsAgent

class A2AModule:
    def __init__(self, host: str, port: int, agent: LatestNewsAgent):
        skill = AgentSkill(
            id="latest_news_skill",
            name="Get Latest News",
            description="Provides the latest news updates.",
            tags=["news", "updates"],
        )
        agent_card = AgentCard(
            name="Latest News Agent",
            description="An agent that provides the latest news updates.",
            url=f"http://{host}:{port}",
            version="1.0.0",
            default_input_modes=["text"],
            default_output_modes=["text"],
            capabilities=AgentCapabilities(),
            skills=[skill],
        )
        request_handler = DefaultRequestHandler(
            agent_executor=LatestNewsAgentExecutor(agent),
            task_store=InMemoryTaskStore(),
        )
        self.app = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=request_handler,
        )

    def get_starlette(self):
        return self.app.build()
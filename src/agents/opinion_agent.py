from typing import List
from pydantic import BaseModel
import pydantic_ai

from ..config import settings
from ..database import get_db
from ..models.user_content import UserContent


class Opinion(BaseModel):
    topic: str
    opinion: str
    style_notes: str


class OpinionAgent:
    def __init__(self):
        with open("system_prompt.md", "r") as f:
            system_prompt = f.read()
        self.agent = pydantic_ai.Agent(
            "openai:gpt-4o-mini", system_prompt=system_prompt, result_type=List[Opinion]
        )

    async def generate_opinions(self, topics: List[str]) -> List[Opinion]:
        # Fetch user content from DB
        user_content = []
        async for session in get_db():
            result = await session.execute(UserContent.__table__.select().limit(10))
            items = result.scalars().all()
            user_content = [item.content for item in items]

        context = "\n".join(user_content)

        # Use agent to generate opinions on topics
        prompt = f"Based on this user content: {context}\nGenerate opinions on these topics: {', '.join(topics)}"

        # For simplicity, mock LLM call; in real, use agent.run
        opinions = []
        for topic in topics:
            opinion = f"Opinion on {topic}: As per my style, this is interesting."
            opinions.append(
                Opinion(topic=topic, opinion=opinion, style_notes="Confident, technical, anti-hype")
            )
        return opinions

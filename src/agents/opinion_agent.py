from typing import List
from pydantic import BaseModel
from pydantic_ai import Agent

from ..database import get_db
from ..models.user_content import UserContent


class Opinion(BaseModel):
    topic: str
    opinion: str
    style_notes: str


with open("system_prompt.md", "r") as f:
    system_prompt = f.read()

opinion_agent = Agent("openai:gpt-4o-mini", system_prompt=system_prompt)


async def generate_opinions(topics: List[str]) -> List[Opinion]:
    # Fetch user content from DB
    user_content = []
    async for session in get_db():
        result = await session.execute(UserContent.__table__.select().limit(10))
        items = result.scalars().all()
        user_content = [item.content for item in items]

    context = "\n".join(user_content)

    # Use agent to generate opinions on topics
    prompt = f"Based on this user content: {context}\nGenerate opinions on these topics: {', '.join(topics)}"

    result = await opinion_agent.run(prompt)
    return result.data

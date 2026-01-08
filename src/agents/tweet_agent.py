from typing import List
from pydantic import BaseModel
from pydantic_ai import Agent

from ..config import settings
from .research_agent import HotTopic
from .opinion_agent import Opinion


class Tweet(BaseModel):
    text: str
    position: int


class TweetThread(BaseModel):
    tweets: List[Tweet]


tweet_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a tweet generator for viral content. Create engaging threads (up to max length) based on topics and opinions. Use questions, hooks, and anti-hype style.",
    result_type=TweetThread,
)


async def generate_thread(topic: HotTopic, opinion: Opinion) -> TweetThread:
    prompt = f"Generate a Twitter thread on topic: {topic.title} ({topic.url}). Opinion: {opinion.opinion}. Max length: {settings.max_thread_length}"

    result = await tweet_agent.run(prompt)
    return result.data

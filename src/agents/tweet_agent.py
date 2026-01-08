from typing import List
from pydantic import BaseModel
import pydantic_ai

from ..config import settings
from .research_agent import HotTopic
from .opinion_agent import Opinion


class Tweet(BaseModel):
    text: str
    position: int


class TweetThread(BaseModel):
    tweets: List[Tweet]


class TweetAgent:
    def __init__(self):
        self.agent = pydantic_ai.Agent(
            "openai:gpt-4o-mini",
            system_prompt="You are a tweet generator for viral content. Create engaging threads (up to max length) based on topics and opinions. Use questions, hooks, and anti-hype style.",
            result_type=TweetThread,
        )

    async def generate_thread(self, topic: HotTopic, opinion: Opinion) -> TweetThread:
        prompt = f"Generate a Twitter thread on topic: {topic.title} ({topic.url}). Opinion: {opinion.opinion}. Max length: {settings.max_thread_length}"

        # Mock for now
        tweets = [
            Tweet(text=f"Thread on {topic.title}: {opinion.opinion[:100]}...", position=0),
            Tweet(text=f"Check it out: {topic.url}", position=1),
        ]
        return TweetThread(tweets=tweets[: settings.max_thread_length])

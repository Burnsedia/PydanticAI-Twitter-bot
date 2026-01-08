from typing import List
import tweepy
import asyncio
from pydantic_ai import Agent, tool

from ..config import settings
from ..database import get_db
from ..models.tweet import Tweet as DBTweet, TweetPydantic
from .tweet_agent import Tweet


posting_client = tweepy.Client(
    bearer_token=settings.twitter_bearer_token,
    consumer_key=settings.twitter_consumer_key,
    consumer_secret=settings.twitter_consumer_secret,
    access_token=settings.twitter_access_token,
    access_token_secret=settings.twitter_access_token_secret,
)


@tool
async def post_initial_tweet(text: str) -> str:
    """Post the initial tweet in a thread."""
    try:
        response = await asyncio.to_thread(posting_client.create_tweet, text=text)
        tweet_id = str(response.data["id"])

        # Save to DB
        db_tweet = DBTweet.from_pydantic(
            TweetPydantic(text=text, thread_position=0, thread_id=tweet_id, status="posted")
        )
        async for session in get_db():
            session.add(db_tweet)
            await session.commit()

        return f"Posted initial tweet: {tweet_id}"
    except Exception as e:
        # Save failed
        db_tweet = DBTweet.from_pydantic(
            TweetPydantic(text=text, thread_position=0, status="failed")
        )
        async for session in get_db():
            session.add(db_tweet)
            await session.commit()
        return f"Failed to post initial tweet: {e}"


@tool
async def post_reply_tweet(text: str, reply_to_id: str) -> str:
    """Post a reply tweet in a thread."""
    try:
        response = await asyncio.to_thread(
            posting_client.create_tweet, text=text, in_reply_to_status_id=reply_to_id
        )
        tweet_id = str(response.data["id"])

        # Save to DB
        db_tweet = DBTweet.from_pydantic(
            TweetPydantic(text=text, thread_position=1, thread_id=reply_to_id, status="posted")
        )
        async for session in get_db():
            session.add(db_tweet)
            await session.commit()

        return f"Posted reply tweet: {tweet_id}"
    except Exception as e:
        # Save failed
        db_tweet = DBTweet.from_pydantic(
            TweetPydantic(text=text, thread_position=1, status="failed")
        )
        async for session in get_db():
            session.add(db_tweet)
            await session.commit()
        return f"Failed to post reply tweet: {e}"


posting_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a Twitter posting agent. Use tools to post tweet threads. Start with initial tweet, then reply tweets. Handle errors gracefully. Return list of posted tweet IDs.",
    result_type=List[str],
    tools=[post_initial_tweet, post_reply_tweet],
)


async def post_thread_via_agent(thread: List[Tweet]) -> List[str]:
    """Post a thread using the PydanticAI agent."""
    if not thread:
        return []

    # Prepare thread data
    thread_data = "\n".join([f"Tweet {i + 1}: {tweet.text}" for i, tweet in enumerate(thread)])

    prompt = f"Post this tweet thread:\n{thread_data}\nUse tools to post each tweet in sequence. Return the list of tweet IDs."

    result = await posting_agent.run(prompt)
    return result.data

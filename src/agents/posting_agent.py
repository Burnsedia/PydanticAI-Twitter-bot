from typing import List
import tweepy

from ..config import settings
from ..database import get_db
from ..models.tweet import Tweet as DBTweet, TweetPydantic
from .tweet_agent import Tweet


class PostingAgent:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=settings.twitter_bearer_token,
            consumer_key=settings.twitter_consumer_key,
            consumer_secret=settings.twitter_consumer_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret,
        )

    async def post_thread(self, thread: List[Tweet]) -> List[str]:
        posted_ids = []
        reply_to = None
        for tweet in thread:
            try:
                response = self.client.create_tweet(text=tweet.text, in_reply_to_status_id=reply_to)
                tweet_id = response.data["id"]
                posted_ids.append(str(tweet_id))
                reply_to = tweet_id

                # Save to DB
                db_tweet = DBTweet.from_pydantic(
                    TweetPydantic(
                        text=tweet.text,
                        thread_position=tweet.position,
                        thread_id=str(tweet_id) if tweet.position == 0 else None,
                        status="posted",
                    )
                )
                async for session in get_db():
                    session.add(db_tweet)
                    await session.commit()
            except Exception as e:
                print(f"Error posting tweet: {e}")
                # Mark as failed
                db_tweet = DBTweet.from_pydantic(
                    TweetPydantic(text=tweet.text, thread_position=tweet.position, status="failed")
                )
                async for session in get_db():
                    session.add(db_tweet)
                    await session.commit()
                break
        return posted_ids

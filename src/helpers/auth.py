import tweepy
from config import config


def auth():
    authent = tweepy.OAuthHandler(
            config.consumer_key,
            config.consumer_secret
        )

    authent.set_access_token(
            config.access_token,
            config.access_secret
        )

    return tweepy.API(authent)

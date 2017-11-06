from django.conf import settings
import oauth2 as oauth
import requests

FB_BASE_URL = 'https://graph.facebook.com/v2.5/me'


def login_twitter(access_key, access_secret):
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET

    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    access_token = oauth.Token(key=access_key, secret=access_secret)
    client = oauth.Client(consumer, access_token)

    timeline_endpoint = "https://api.twitter.com/1.1/account/verify_credentials.json"
    return client.request(timeline_endpoint)

    # return json.loads(data.decode())


def login_facebook(access_token):
    url = '{}?fields=id,first_name,last_name,email,picture.type(large)&access_token={}'.format(
        FB_BASE_URL, access_token)
    return requests.get(url)

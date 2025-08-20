from ..config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
import tweepy
import requests
import tempfile
import os
from ..utils.logger import logger


def post_tweet_with_image_url(tweet_text: str, image_url: str,reply_tweet_text = ""):
    # Load API credentials from environment variables
    consumer_key = TWITTER_CONSUMER_KEY
    consumer_secret = TWITTER_CONSUMER_SECRET
    access_token = TWITTER_ACCESS_TOKEN
    access_token_secret = TWITTER_ACCESS_TOKEN_SECRET

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        raise ValueError("Missing Twitter API credentials. Set them as environment variables.")

    # Validate tweet length (280 characters max)
    if len(tweet_text) > 280:
        raise ValueError(f"Tweet text exceeds 280 characters: {len(tweet_text)}")

    # Initialize tweepy.API for v1.1 (media upload)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Initialize tweepy.Client for v2 (tweet posting)
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    try:
        # Verify credentials
        user = client.get_me()
        logger.info(f"Authenticated as: {user.data.username}")

        # Download the image from the URL
        logger.info(f"Downloading image from: {image_url}")
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to download image from {image_url}: Status {response.status_code}")

        # Check content type to ensure it's a supported image
        content_type = response.headers.get("content-type", "").lower()
        if not any(fmt in content_type for fmt in ["image/jpeg", "image/png", "image/gif"]):
            raise ValueError(f"Unsupported image format: {content_type}. Use JPG, PNG, or GIF.")

        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            # Upload image using v1.1 API
            logger.info(f"Uploading image from temporary file: {temp_file_path}")
            media = api.media_upload(filename=temp_file_path)
            media_id = media.media_id
            logger.info(f"Image uploaded successfully, media_id: {media_id}")

            # Post tweet with text and media using v2 API
            response = client.create_tweet(text=tweet_text, media_ids=[media_id])

            initial_tweet_id = response.data['id']

            reply_response = client.create_tweet(
                text=reply_tweet_text,
                in_reply_to_tweet_id=initial_tweet_id,
            )

            logger.info(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
            return response

        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            logger.info(f"Temporary file deleted: {temp_file_path}")

    except tweepy.TweepyException as e:
        logger.error(f"Failed to post tweet: {e}")
        logger.error(f"Full error response: {e.response.text if e.response else 'No response details'}")
        if e.response:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response headers: {e.response.headers}")
        raise RuntimeError(f"Failed to post tweet: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise RuntimeError(f"Unexpected error: {e}")

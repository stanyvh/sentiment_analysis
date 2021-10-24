
"""
This program was written in the third year of my bachelor degree in
business management, majoring in entrepreneurship at the University College
Leuven Limburg in Belgium for my bachelor research.
The goal was to explore the different ways that sentiment analysis can be done.
Due to time constraints for the project, I chose the simplest solution.
An already existing sentiment analyser named TextBlob. In return, I tried to
write as best code I could for someone without any experience.
I enjoyed this project so much that I decided to pursue a master's degree
in computing at the University of Roehampton after finishing my degree in
business management.
"""

# Importing all libraries that will be used.
# regular expression is used to clean the tweets.
# tweepy is used to access Twitter for the tweets.
# TextBlob is the sentiment analyser used in this program.
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    """
    This class contains all function to work with the Twitter API,
    and to analyse tweets. We call these function in our 'main' program
    at the bottom.
    """

    def __init__(self):
        """
        In this function the authentication for the Twitter API is formed.
        To use this code you will have to provide your own private Twitter
        API codes.
        """
        # API keys en tokens
        consumer_key = '0EjBpPNYidDrSpyHKJhNCkVBf'
        consumer_secret = 'l9iuDqRE3kiIzwfE4WrxgyQyrGR2fpIlPj8heqd8IAeRiT9UbQ'
        access_token = '1338853510268370945-WsaeVs984jIg3n0lRHoEEousvJcmtA'
        access_token_secret = 'ZV5T9y1aHdZAPpo8mIw4UuZ5kA7rn3nGj7Ohe95bAapTZ'

        """
        Authentication https://docs.tweepy.org/en/latest/getting_started.html
        try/except statement is used in case the authentication failed.
        An error message is portrayed to the user. 
        """
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except: print("Error: Authentication failed.")

    # The function that cleans the tweets.
    def clean_tweet(self, tweet):
        """
        This function cleans the tweets by deleted links and special
        characters.
        """
        return ' '.join(re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
            " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        """
        This function needs a tweet and gets the sentiment using textblob.
        """
        analyse = TextBlob(self.clean_tweet(tweet))
        if analyse.sentiment.polarity > 0:
            return 'positive'
        elif analyse.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):
        """
        This function retrieves tweets from Twitter
        """
        # Creating the list tweets that does not contain any tweets.
        tweets = []
        # Because of the try/except statement, the error is shown when raised.
        try:
            # api.search() was updated to api.search_tweets,
            # changed on 24 okt 2021.
            fetched_tweets = self.api.search_tweets(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                # we cancel out re tweets because counting them would give
                # a wrong perception.
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepError as error:
            print("Error: " + str(error))

def main():
    """
    This is the 'main' function and our core program that uses everything
    in the above class to execute the program.
    First we ask which brand the user wants to research, then how many tweets
    have to be analysed.
    """
    api = TwitterClient()
    # Asking input from the user.
    tweets = api.get_tweets(query = input("Brand: "),
                            count = input("Number of tweets: "))
    # The positive tweets are every tweet in the tweets list,
    # where the sentiment is classified as positive.
    positive_tweets = [tweet for tweet in tweets
                       if tweet['sentiment'] == 'positive']
    # The number of positive tweets divided by the total tweets times 100
    # gives us the percentage of positive tweets. Rounded to 2 decimal places.
    ptweets = round(100 * len(positive_tweets) / len(tweets), 2)
    print("Sentiment analysis")
    print("The percentage of positive tweets is: {} %".format(ptweets))

    # The negative tweets are every tweet in the tweets list,
    # where the sentiment is classified as negative.
    negatieve_tweets = [tweet for tweet in tweets
                        if tweet['sentiment'] == 'negative']
    # The number of negative tweets divided by the total tweets times 100
    # gives us the percentage of negative tweets. Rounded to 2 decimal places.
    ntweets = round(100 * len(negatieve_tweets) / len(tweets), 2)
    print("The percentage of negative tweets is: {} %".format(ntweets))

    # the number of tweets - the negative tweets + the positive tweets
    # divided by the number of tweets gives us the remaining tweets that
    # are classified as neutral.
    neutweets = round(100 * (len(tweets)
                            - (len(negatieve_tweets) + len(positive_tweets)))
                     / len(tweets), 2)
    print("The percentage of neutral tweets is: {} %".format(neutweets))

# Here we run the our 'main' funtion.
if __name__ == "__main__":
    main()
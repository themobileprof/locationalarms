from webbrowser import get
import requests
import os
import json
import environ
from .models import EventTag
from .models import TweetProcessor
from .models import Location

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


class Tweets:
    # To set your environment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    bearer_token = env("TWITTER_BEARER_TOKEN")

    search_url = "https://api.twitter.com/2/tweets/search/recent"

    

    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    # 
    def __init__(self) -> None:
        self.query_params = {'query': '(' + self.get_locations() + ') lang:en -is:retweet','tweet.fields': 'author_id'}

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def connect_to_endpoint(self):
        response = requests.get(self.search_url, auth=self.bearer_oauth, params=self.query_params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    # Get the right event to include in this twitter search request
    def get_events(self):
        event_list = EventTag.objects.all()
        event_number = self.get_TweetProcessor()%len(event_list)

        for event in event_list.iterator():
            if (event.id == event_number):
                events = event.tag

                for synonym in event.synonyms.split(","):
                    events = events + " OR " + synonym

        return events

    # Get locations from DB
    def get_locations(self):
        location_list = Location.objects.all()

        locations = "Nigeria OR Lagos"

        for location in location_list.iterator():
            locations += " OR " + location.location

        return locations

    # Get search number and add one more to it,
    # This is used to determine which tag to process now
    def get_TweetProcessor(self):
        tweet_search_number = TweetProcessor.objects.get(pk=1)
        current_number = tweet_search_number.process_number

        tweet_search_number.process_number=tweet_search_number.process_number+1
        tweet_search_number.save()

        return current_number



def main():
    

    search_tweets = Tweets()
    json_response = search_tweets.connect_to_endpoint()
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
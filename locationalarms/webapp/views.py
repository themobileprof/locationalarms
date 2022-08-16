from django.shortcuts import render
from django.http import HttpResponse
# import json
from .tweets import Tweets

# Create your views here.
def collect(request):
    # ## Get event and synonym from the database
    # query_params = {'query': '(<event> OR <event>) place_country:NG lang:en -is:retweet','tweet.fields': 'author_id'}

    search_tweets = Tweets()
    json_response = search_tweets.connect_to_endpoint()

    # ## Store tweets in a database

    # print(json.dumps(json_response, indent=4, sort_keys=True))

    return HttpResponse(json_response)


def process(request):
    return HttpResponse("Tweets processor.")
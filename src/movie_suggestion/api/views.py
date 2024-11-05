from django.shortcuts import render
import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_suggestion.settings import OMDB_API_KEY, OMDB_BASE_URL


# Create your views here.
def index(request):
    return HttpResponse("Your api is running!")


@api_view(['GET'])
def fetch_movies(request, ):
    # Define the api parameters
    params = querydict_to_params(request.GET)
    # OMDB API request
    response = requests.get(OMDB_BASE_URL, params=params)
    if response.status_code == 200:
        # Get the JSON response from OMDB api
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Something went wrong. Failed to fetch data from OMDB'},
                        status=status.HTTP_400_BAD_REQUEST)


def querydict_to_params(querydict):
    # Convert QueryDict to a normal Python dictionary
    params = dict(querydict)

    # Extract the first element from the list
    params = {key: value[0] for key, value in params.items()}

    # Add the API key to the params
    params['apikey'] = OMDB_API_KEY

    return params

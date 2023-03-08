import json
import pandas as pd
import requests
import pytest


import dotenv
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

client_key = os.getenv("CLIENT_KEY")


def popular_events(client_key, city):
    
    """"
    
    A function that returns upcoming concerts in a given city, ranked by popularity.
    
    Parameters
    -------------
    client_key: the API key needed to authenticate the user and gain access to SeatGeek's API
    
    city: any city the user is interested in searching


    Output
    ----------
    >>> popular_events(client_id, 'Los Angeles')
    
    
        Artists   | Scores
    0  Lizzo      | 0.47          
    1  Al Franken | 0.32         
    
    
    """

    # GET request
    
    BASE = 'https://api.seatgeek.com/2/events?client_id='
    REQUEST = BASE + client_key
    r = requests.get(REQUEST, params={'venue.city' : city, 'type' : 'concert'})
#     print(json.dumps(r2.json(), indent=2))

    # Checking GET status
    print(f'Status Code: {r.status_code}')
    
    
    # Converting json to obtain necessary data
    city = r.json()
    data = city['events']
    data

    # Iterating to get the name of the performers
    names = []

    for d in data:
    
        for a in d['performers']:
            result = a['name']
            names.append(result)
            
    # Iterating to get the scores (popularity ranking) of each performer based on ticket sales
    
    score = []

    for d in data:
    
        for a in d['performers']:
            rate = a['score']
            score.append(rate)
    
    # Creating dataframe with names and ranking of concerts
    
    df = pd.DataFrame(names, columns = ['Artists'])
    df['Scores'] = score
    df.sort_values(by = ['Scores'], ascending = False) # this tells us the most popular upcoming concerts being searched right now

    return df



def cheap_tix(client_key, price, artist):
    
    """
    This function returns a dataframe of the cheapest tickets of an upcoming event of a specific artist.
    
    Parameters
    -----------
    
    client_key : client_id authentication
    
    price : the highest price a user is willing to pay for the event
    
    artist : any artist that has concerts listed on SeatGeek already. should be written out in lower case, and
                if the artist's name has more than one word, separate each word with a dash
    
    
    Output
    ----------
    The function will output a dataframe of the artist's lowest priced ticket, the location of the event,
    the title of the event, and a link to the event. 
    
    
    Example
    ---------
    >>> cheap_tix(client_id, 500, 'sabrina-carpenter')
    
        Artist           | Lowest Price | Location         | Title             | Link
    0  Sabrina Carpenter | 90           | Tulsa Theater    | Sabrina Carpenter | https://seatgeek.com/sabrina-carpenter-tickets...
    1  Sabrina Carpenter | 475          | Ryman Auditorium | Sabrina Carpenter | https://seatgeek.com/sabrina-carpenter-tickets...
    
   
    """
    
    # GET request
    
    BASE = 'https://api.seatgeek.com/2/events?client_id='
    REQUEST = BASE + client_key
    r = requests.get(REQUEST, params={'highest_price.lte' : price, 'performers.slug' : artist})

    
    # Checking GET status
    print(f'Status Code: {r.status_code}')
    
    
    # Converting json to obtain necessary data
    tix = r.json()
    data = tix['events']
    data
    
    # Iterating to get the title of the event
    
    title = []

    for t in data:
        result = t['title']
        title.append(result)

    # Iterating to get the links for each event
    
    link = []

    for t in data:
        result = t['url']
        link.append(result)
        
    # Iterating to get the location of each event
    
    place = []

    for t in data:
        result = t['venue']['name']
        place.append(result)
        
    # Iterating to get the name of the performer
    
    name = []

    for t in data:

        for a in t['performers']:
            result = a['name']
            name.append(result)
            
    # Iterating to get the lowest price of each event
    
    price = []

    for t in data:
        result = t['stats']['lowest_price']
        price.append(result)
        

    # Iterating to get the date of the event
    
    time = []

    for t in data:
        result = t['datetime_utc']
        time.append(result)
     
    
    # Making dataframe with lists from above
    
    cheap = pd.DataFrame(name, columns = ['Artist Name'])
    cheap['Date'] = time
    cheap['Lowest Price'] = price
    cheap['Location'] = place
    cheap['Title'] = title
    cheap['Link'] = link
    
    return cheap


def recommend_me(client_key, artist, postal):
    
    """"
    This function uses the events endpoint and recommendations endpoint to recommend the user upcoming events 
    related to a performer and location of their choosing. 
    
    This function will have two GET requests: the first is to retrieve the performer id of the artist of the
    user's choosing, and the second will generate a recommendations dataframe related to that artist.


    Parameters
    ------------
    client_key : client_id authentication key
    
    artist : an artist of the user's choosing. must already have concerts listed on SeatGeek
    
    postal : the postal code of any city
    
    
    Output
    -----------
    The function will generate two outputs: 
    1) the status code of each GET request, and 
    2) a dataframe of recommendations
    
    
    Example
    ---------
    >>> recommend_me(client_key, 'adele', '90001')
    
    Status Code: 200
    
           Names           | Type            | Links
    0  Cali Vibes Festival | music festival  | https://seatgeek.com/cali-vibes-festival-tickets
    1  Damian Marley       | band            | https://seatgeek.com/damian-marley-tickets
    
    """
    
    # First GET request to find associated performer_id
    
    BASE1 = 'https://api.seatgeek.com/2/events?client_id='
    REQUEST1 = BASE1 + client_key
    r = requests.get(REQUEST1, params={'performers.slug' : artist})

    
    # Checking first request status
    
    print(f'Status Code: {r.status_code}')
    
    # To extract a performer's id

    perf = r.json()
    peid = perf['events']

    idn = []

    for t in peid:

        for a in t['performers']:
            result = a['id']
            idn.append(result)

    id1 = idn[1] # using the second positional value because they might be an opener for an artist
    
    
    
    # Second GET request- this time for the actual recommendation, with the ID found previously
    
    BASE2 = 'https://api.seatgeek.com/2/recommendations?client_id='
    REQUEST2 = BASE2 + client_key
    r2 = requests.get(REQUEST2, params={'performers.id': id1, 'postal_code': postal})
    
    # Checking first request status
    
    print(f'Status Code: {r2.status_code}')
    
    # Converting json
    rx = r2.json()
    recs = rx['recommendations']
    recs
    
    # Iterating to find recommended performances
    
    performing = []

    for r in recs:
        result = r['event']['performers']
        for e in result:  
            pp = e['name']
            performing.append(pp)
    
    # Iterating to find the type of performances
    
    typep = []

    for r in recs:
        result = r['event']['performers']
        for e in result:  
            pp = e['type']
            typep.append(pp)

    # Iterating to find the links for each performance
    
    url = []

    for r in recs:
        result = r['event']['performers']
        for e in result:  
            pp = e['url']
            url.append(pp)
    
    
    # Making dataframe
    df = pd.DataFrame(performing, columns = ['Names'])
    df['Type'] = typep
    df['Links'] = url
    return df



def performer_id(client_key, artist):

    """
    This function returns the performer_id of a particular performer on SeatGeek's
    API.


    Parameters
    ------------
    client_key : client_id authentication key

    artist : any artist name


    Output
    --------
    The function will output the id number of the artist.


    Example
    ----------
    >>> performer_id(client_key, 'adele')

    141

    """
    
    # GET request to find associated performer_id
    
    BASE1 = 'https://api.seatgeek.com/2/events?client_id='
    
    # Adding assertion error that causes exception when client_key
        # is set to an integer
    
    if type(client_key) == int:
        raise AssertionError('Client key must be a string')
    else:
    
        REQUEST1 = BASE1 + client_key
        

        r = requests.get(REQUEST1, params={'performers.slug' : artist})

    # To extract a performer's id

    perf = r.json()
    peid = perf['events']

    idn = []

    for t in peid:

        for a in t['performers']:
            result = a['id']
            idn.append(result)

    id1 = idn[1] # using the second positional value because they might be an opener for an artist
    return id1


def city_status(client_key, city):

    """
    This function returns the status code for city-specific concerts.

    Parameters
    -------------
    client_key : client_id authentication key

    city : city name


    Output
    ---------
    This function will output the status code of the GET request.


    Example
    ---------
    >>> city_status(client_key, 'Los Angeles')
    200

    """

    BASE = 'https://api.seatgeek.com/2/events?client_id='
    
    if type(client_key) == int:
        raise AssertionError('Client key must be a string')
    else:

        REQUEST = BASE + client_key

        r = requests.get(REQUEST, params={'venue.city' : city, 'type' : 'concert'})

        if r.status_code != 200:
            raise AssertionError("Error connecting with events endpoint")
        else:
            return r.status_code
        



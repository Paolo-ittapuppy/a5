# lastfm.py
# 67a0e9526f7a52637dde3a5539499e56
# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

import json
from urllib import request, error
from zipfile import ZIP_MAX_COMMENT
import random
import WebAPI

class LastFM(WebAPI.WebAPI):

    apiKey = None
    jsonDictionary = None
    topArtists = {}

    
    def _setDataArtists(self):
        data = self.jsonDictionary
        self.topArtists = {}
        for i in data['artists']['artist']:
            self.topArtists[i['playcount']] = i['name']
        

    #uses the get top artists api method from Last fm to get a list of the top 50 artists. 
    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        urlArt = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={self.apiKey}&limit=50&format=json'
        
        lastFM_obj = self._download_url(urlArt)

        if lastFM_obj is not None:
            
            self.jsonDictionary = lastFM_obj
            self._setDataArtists()

        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes

    #obtains the artist with the highest playcount
    def topArtist(self):
        playcounts = self.topArtists.keys()
        playcounts = [int(x) for x in playcounts]
        playcounts = sorted(playcounts, reverse=True)
        return self.topArtists[str(playcounts[0])]

    
    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        spl = message.split('@lastfmRand')
        artistsList = list(self.topArtists.values())
        transcluded = f'{artistsList[random.randint(0,49)]}'.join(spl)
        spl = transcluded.split('@lastfm')
        transcluded = f'{self.topArtist()}'.join(spl)
        return transcluded
        
        #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
        pass

# Replace the following placeholders with your information.
# Paolo Andrew Urani
# Uranip@uci.edu
# 24555312

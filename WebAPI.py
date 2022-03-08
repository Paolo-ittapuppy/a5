# webapi.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Paolo Andrew, Manalo, Urani
# Uranip@uci.edu
# 24555312

from abc import ABC, abstractmethod
from urllib import request , error
import json

class WebAPI(ABC):
  apiKey = None
  def _download_url(self, url: str) -> dict:
    #TODO: Implement web api request code in a way that supports ALL types of web APIs
    response = None
    r_obj = None
    
    try:
        response = request.urlopen(url)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except error.HTTPError as e:
        print('Failed to download contents of URL')
        if e.code == 401:
            print('Invalid authentication')
        if e.code == 503:
            print('The API is unable to return information at the moment')
        #print('Status code: {}'.format(e.code))
    except error.URLError as e:
        print('No internet connection')
    except json.JSONDecodeError as e:
        print('Invalid json data retrieved')
    

    finally:
        if response != None:
            response.close()
    
    return r_obj
	
  def set_apikey(self, apikey:str) -> None:
    self.apiKey = apikey
    pass
	
  @abstractmethod
  def load_data(self):
    pass
	
  @abstractmethod
  def transclude(self, message:str) -> str:
    pass

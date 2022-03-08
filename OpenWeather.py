# openweather.py
#Key for weather : 47c57598a8dea1145b37db4121f67161
# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python
import json
import urllib
from urllib import request, error
from zipfile import ZIP_MAX_COMMENT
import WebAPI

class OpenWeather(WebAPI.WebAPI):

    apiKey = None
    jsonDictionary = None
    zipcode = None
    ccode = None
    temperature = None
    high_temperature = None
    low_temperature = None
    longitude = None
    latitude = None
    description = None
    humidity = None
    sunset = None
    city = None

    def __init__(self, zip = '92697', ccode = 'US') -> None:
        self.zipcode = zip
        self.ccode = ccode


    def _setData(self):
        data = self.jsonDictionary
        #print(type(data['weather']))
        self.temperature = data['main']['temp']
        self.high_temperature = data['main']['temp_max']
        self.low_temperature = data['main']['temp_min']
        self.longitude = data['coord']['lon']
        self.latitude = data['coord']['lat']
        self.description = data['weather'][0]['description']
        self.humidity = data['main']['humidity']
        self.sunset = data['sys']['sunset']
        self.city = data['name']
    

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #try:
        url = f'http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&units=imperial&appid={self.apiKey}'
        print(url)
        weather_obj = self._download_url(url)

        if weather_obj is not None:
            #
            self.jsonDictionary = weather_obj
            self._setData()
            
        #except:
        #    print('sum error shit right here')
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        spl = message.split('@weather')
        transclude = f'{self.description} at {self.temperature} degrees F'.join(spl)

        return transclude
        #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
# Replace the following placeholders with your information.

if __name__ == '__main__':
    zipcode = '92697'
    open_weather = OpenWeather(zipcode, 'US')
    open_weather.set_apikey('47c57598a8dea1145b37db4121f67161')
    open_weather.load_data()
    zipcode = '92697'
    #print(open_weather.jsonDictionary)
    
    print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
    print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
    print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
    print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
    print(f"The current weather for {zipcode} is {open_weather.description}")
    print(f"The current humidity for {zipcode} is {open_weather.humidity}")
    print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")

    print(open_weather.transclude('testing 123 @weather today'))

# NAME
# EMAIL
# STUDENT ID


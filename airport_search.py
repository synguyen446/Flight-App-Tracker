# This class is responsible for searching for aiports that are within the 250km radius of input city.

import requests

class AirportSearch():
    def __init__(self) -> None:
        # Initialize API endpoints and keys
        self.airport_search_endpoint = 'https://api.tequila.kiwi.com/locations/radius'
        self.airport_search_apikey = '2xEuRmzvBXXCSiYxmgqKsnvqIqVY9at4'
        self.lon_lat_search_endpoint = 'http://api.openweathermap.org/geo/1.0/direct'
        self.lon_lat_apikey = '8b8e17db1edfda1ee33be825d5c1f9c7'

    def search(self, city: str) -> list:
        # Get city coordinates and search for nearby airports
        location = self.__get_lon_lat(city)
        if location:
            airport_search_headers = {'apikey': self.airport_search_apikey}
            airport_search_query = {'lon': location[0], 'lat': location[1]}
            response = requests.get(url=self.airport_search_endpoint, headers=airport_search_headers, params=airport_search_query)
            airports = response.json()['locations'][0]['alternative_departure_points']
            airports_info = [airport['id'] for airport in airports if airport['duration']/3600 < 2 and len(airport['id']) < 4]          # Only select airports if they are within the 2 hours radius.
            return airports_info                                                                                                        # and airport code has less than 4 characters.
        return None

    def __get_lon_lat(self, city) -> tuple:
        # Get longitude and latitude for a city
        lon_lat_query = {'appid': self.lon_lat_apikey, 'q': city}
        response = requests.get(url=self.lon_lat_search_endpoint, params=lon_lat_query)
        try:
            data = response.json()[0]
            return (data['lon'], data['lat'])
        except:
            return None

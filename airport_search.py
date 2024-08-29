import requests

# this class will return all airports within the radius of 250km

class AirportSearch():
    def __init__(self) -> None:
        self.airport_search_endpoint= 'https://api.tequila.kiwi.com/locations/radius'   # address of request to search for airport
        self.airport_search_apikey= '2xEuRmzvBXXCSiYxmgqKsnvqIqVY9at4'                  # apikey for every request
        self.lon_lat_search_endpoint='http://api.openweathermap.org/geo/1.0/direct'     # address of request to search for location
        self.lon_lat_apikey='8b8e17db1edfda1ee33be825d5c1f9c7'                          # apikey for every request

    
    def search(self,city:str):

        location = self.__get_lon_lat(city)
        if location:
            airport_search_headers = {                                      
                'apikey':self.airport_search_apikey
            }
        
            airport_search_query = {
                'lon':location[0],
                'lat':location[1],
            }

            response = requests.get(url = self.airport_search_endpoint,                 #send request to tequilla kiwi 
                                    headers= airport_search_headers,                    #to get airports information
                                    params= airport_search_query)               
            airports = response.json()['locations'][0]['alternative_departure_points']  #filter so that only return aiports

            airports_info =[]                           # An empty list to store all available airports,
                                                        # and its information
            for airport in airports:
                if airport['duration']/3600 < 2 and len(airport['id'])<4:
                    airports_info.append(airport['id'])

            return airports_info
        else:
            return None

    def __get_lon_lat(self,city):

        lon_lat_query ={
            'appid':self.lon_lat_apikey,
            'q':city,
        }

        response = requests.get(url = self.lon_lat_search_endpoint, 
                                params=lon_lat_query)
        try:
            data = response.json()[0]
        except:
            return None
        else:
            lon = data['lon']
            lat = data['lat']
            return [lon , lat]

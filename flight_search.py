import requests
from flight_data import FlightData
from typing import Iterator

class FlightSearch:
    
    # Class responsible for checking available flights with given parameters.


    def __init__(self, originCity: str, destination: str, departure_date: str, 
                 return_date: str, cabin: str = None) -> None:
        """
        Initializes the FlightSearch object with search parameters.

        Sets up the API key, endpoint, headers, and request parameters 
        based on whether the search includes a return date.
        """
        self._apikey = '2xEuRmzvBXXCSiYxmgqKsnvqIqVY9at4'
        self._endpoint = "https://api.tequila.kiwi.com/v2/search"

        self._header = {
            'apikey': self._apikey,
        }
        
        # Set parameters for a round-trip flight
        if len(return_date) > 0:
            self.return_date = True
            self._params = {
                'fly_from': originCity,          # Origin airport code
                'fly_to': destination,           # Arrival airport code
                'date_from': departure_date,     # Departure date from
                'date_to': departure_date,       # Departure date to
                'return_from': return_date,      # Return date from
                'return_to': return_date,        # Return date to
            }
        else:
            # Set parameters for a one-way flight
            self.return_date = False
            self._params = {
                'fly_from': originCity,          # Origin airport code
                'fly_to': destination,           # Arrival airport code
                'date_from': departure_date,     # Departure date from
                'date_to': departure_date,       # Departure date to
                'selected_cabins': cabin,        # Optional cabin selection
            }

    def check_flight(self) -> Iterator[FlightData]:
        """
        Sends a request to the flight search API and yields FlightData 
        objects for each flight found.

        Parses the response to extract flight information and creates 
        FlightData objects.
        """
        response = requests.get(url=self._endpoint, params=self._params, 
                                headers=self._header)
        
        for i in range(len(response.json()['data'])):
            data = response.json()['data'][i]
            
            # Determine the return date for round-trip flights
            if self.return_date:
                return_date = data['route'][1]['local_departure']
            else:
                return_date = None
            
            # Combine airlines into a single string if necessary
            if not isinstance(data['airlines'], str):
                airlines = ' - '.join(data['airlines'])
            
            # Create a FlightData object for each flight
            flight = FlightData(
                data['flyFrom'],
                data['cityFrom'],
                data['flyTo'],
                data['cityTo'],
                data['local_departure'],
                data['local_arrival'],
                return_date,
                return_date,
                data['price'],
                airlines,
                data['duration']
            )
            yield flight
        
        return None

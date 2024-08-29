import requests
from flight_data import FlightData
from datetime import datetime as dt

class FlightSearch:
    def __init__(self,originCity,destination,departure_date,return_date,cabin = None) -> None:
        self._apikey = '2xEuRmzvBXXCSiYxmgqKsnvqIqVY9at4'
        self._endpoint = "https://api.tequila.kiwi.com/v2/search"

        self._header = {
            'apikey':self._apikey,
        }
        if len(return_date) >0:
            self.return_date = True
            self._params = {
                'fly_from': originCity,          #origin airport code
                'fly_to':destination,            #arrival airport code
                'date_from':departure_date,      #departure date from
                'date_to':departure_date,        #departure date to      
                'return_from':return_date,       #return date from
                'return_to':return_date,         #return date to  
                # 'selected_cabins': cabin,      
                # 'one_for_city':1,
                # 'max_stopovers' : 0,
            }
            
        else: 
             self.return_date = False
             self._params = {
                'fly_from': originCity,          #origin airport code
                'fly_to':destination,            #arrival airport code
                'date_from':departure_date,      #departure date from
                'date_to':departure_date,        #departure date to  
                'selected_cabins': cabin,          
                # 'one_for_city':1,
                # 'max_stopovers' : 0,
            }

    def check_flight(self):
        response = requests.get(url = self._endpoint, params= self._params,
                                headers= self._header)
        
        for i in range(len(response.json()['data'])):
                data = response.json()['data'][i]
                if self.return_date:
                    return_date = data['route'][1]['local_departure']
                else:
                    return_date = None
                
                if not isinstance(data['airlines'],str):
                    airlines = ' - '.join(data['airlines'])

                flight = FlightData(data['flyFrom'],
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
        
        
        
        
    
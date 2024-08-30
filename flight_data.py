 # This class is responsible for structuring the flight data.

from datetime import datetime as dt

class FlightData:
   
    def __init__(self,
                 origin_airport:str,
                 origin_city:str,
                 destination_airport:str,
                 destination_city:str,
                 origin_depart_date:str,
                 origin_arrival_date:str,
                 return_depart_date:str,
                 return_arrival_date:str,
                 price:str,
                 airlines:str,
                 duration:str) -> None:

        
        self.origin_airport = f'{origin_airport} - {origin_city}'
        self.destination_airport = f'{destination_airport} - {destination_city}'
        self.depart_date = origin_depart_date
        self.arrival_date = origin_arrival_date
        self.return_date = return_depart_date
        self.return_arrival_date = return_arrival_date
        self.price = price
        self.airlines = airlines
        self.duration_departure = duration['departure']
        self.duration_return = duration['return']
        self.duration_total = duration['total']

        self.format()

    def format(self):
        if not isinstance(self.airlines,str):
                    self.airlines = ' - '.join(self.airlines)

        local_departure = dt.fromisoformat(self.depart_date)
        self.depart_date = f'{local_departure.date()} - \
{local_departure.time()}'
                
        local_arrival = dt.fromisoformat(self.arrival_date)
        self.arrival_date = f'{local_arrival.date()} - \
{local_arrival.time()}'

        if self.return_date:       
                local_redeparture = dt.fromisoformat(self.return_date)
                self.return_date = f'{local_redeparture.date()} - \
        {local_redeparture.time()}'
                        
                local_rearrival = dt.fromisoformat(self.return_arrival_date)
                self.return_arrival_date = f'{local_rearrival.date()} - \
        {local_rearrival.time()}'
                
    def __str__(self):
        if self.return_date:
                result= f"From: {self.origin_airport} To: {self.destination_airport} ==== From {self.destination_airport} To: {self.origin_airport} \n\
        {self.depart_date}, {self.arrival_date} ==== {self.return_date}, {self.return_arrival_date}\n\
        Duration: {float(self.duration_departure)/3600:.2f} hours ==== Duration: {float(self.duration_return)/3600:.2f} hours\n\
        {self.price},{self.airlines}, total duration: {float(self.duration_total)/3600:.2f} hours"
                
        else:
              result= f"From: {self.origin_airport} To: {self.destination_airport}\n\
        {self.depart_date}, {self.arrival_date}\n\
        Duration: {float(self.duration_departure)/3600:.2f} hours\n\
        {self.price},{self.airlines}, total duration: {float(self.duration_total)/3600:.2f} hours"
        return result

import smtplib
from flight_data import FlightData

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self) -> None:
        self.my_gmail = 'nsn131203@gmail.com'
        self.password = 'dodu xyty bkrt ftye'

    def send_alert(self,flight:FlightData):
        contents = f'Subject: Ring Ring Cu Bap may bay🌽✈️✈️\n\n\
Sent from Cu Bappp - Currently ${flight.price}\
 to fly from {flight.origin_airport} to {flight.destination_airport},\
 from {flight.depart_date} to {flight.return_date}'

        with smtplib.SMTP('smtp.gmail.com',587,timeout= 120) as connection:
            connection.starttls()
            connection.login(user=self.my_gmail, password=self.password)
            connection.sendmail(from_addr=self.my_gmail,
                                    to_addrs='annlee43603@gmail.com', msg=contents.encode('utf-8'))
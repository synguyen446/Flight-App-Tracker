# Flight App Tracker
 
A Python application implemented using ```ttkbootstrap``` for user interface, and ```requests``` for requesting API endpoint.
The user is prompted to input the origin city and the destination city. The program will return every airport within the proximity of the inputed cities. Then, every airport will be used as an input so that a list of available flight will be displayed to the user from all selected airports.

## Guide
The program is yet to be at its prestine stage. There will be bugs, errors that could crash the program. There are also still missing features.
### Required Field
- Origin City (left most entry)<br>
- Destination City (Right most entry)<br>
- Departing date (top datetime entry)<br>
- Return date (bottom datetime entry), only required if chose roundtrip, will be ignored otherwise.<br>
**The departing date will need to be earlier than the return date, otherwise the program will produce an error.**
## Installation
Install ttkboostrap for enhanced user interface.
```bash
pip install tkkbootstrap
```
Install requests for making request to an API endpoint. 
```bash
pip install requests
```

## Verifying Installation
```bash
pip show "Module Name"
```

## Usage
To start the applcation run main.py. 

## Future Work
- Create exception so that the program will not crash if the required field are empty.<br>
- Implement a function for placing the ticket in bulk, and being able to see ticket price for infant passenger.<br>
- Format the ouput for better user experience.<br>
- Add placeholder for missing entry.<br>

## File
### img
- include all used images
## city_data
- include more than thousands of city entries for searching suggestion system.
### main.py
- Responsible for running the program
### airport_search.py
- Taking city as a paramenter, and return airports within range.
### data_manager.py
- Responsible for formating the the resulting flights and outputing them.
### flight_search.py
- Taking airports as input, and return available flights
### flight_data.py
- Format the data of the flight, including duration, cost, date, and time
### user_interface.py
- Responsible for user interface and experience



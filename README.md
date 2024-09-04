# Flight App Tracker
 
A Python application for searching flights between cities, implemented using the `ttkbootstrap` library for the user interface and `requests` for API calls.
The user is prompted to input the origin city and the destination city. The program will return every airport within the proximity of the inputed cities. Then, every airport will be used as an input so that a list of available flight will be displayed to the user from all selected airports.

## Features

- **City-to-Airport Search**: Find airports within a 250km radius of the origin and destination cities.
- **Flight Search**: Search for available flights between selected airports, based on the input dates and class preferences.
- **User-Friendly Interface**: Interactive UI with input fields for cities, dates, and flight classes.
- **Results Display**: View flight results in a separate, organized window.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python packages: `ttkbootstrap`, `requests`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/flight-tracker-app.git
   cd flight-tracker-app
    ```
2. Install the required packages:
    ```bash
    pip install ttkbootstrap requests Pillow
    ```
3. Run the application:
    ```bash
    python main.py
    ```

### Usage

1. Input the Origin City and Destination City in the corresponding fields.<br>
2. Select the Departing Date and (optional) Return Date.<br>
3. Choose the Flight Class from the dropdown menu.<br>
4. Click Search to find available flights.<br>
5. The results will be displayed in a new window.<br>

### Project Structure

-```airport_search.py```: Handles searching for nearby airports based on city coordinates.
-```data_manager.py```: Manages the display of flight results.
-```flight_data.py```: Structures the flight data.
-```flight_search.py```: Performs the flight search between airports.
-```main.py```: Entry point of the application, integrates all components.
-```user_interface.py```: Handles the graphical user interface.

### Known Issuse

- The application is still in development and may have bugs or missing features
- Ensure that the departing date is earlier than the return date to avoid erros.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

### License

This project is licensed under the MIT License
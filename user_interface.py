import ttkbootstrap as tkk
import tkinter as tk
import json
import datetime as dt
from airport_search import AirportSearch
from flight_search import FlightSearch
from PIL import Image, ImageTk
from data_manager import DataManager

# Define constants for flight classes and their corresponding codes
FLIGHT_CLASSES = ["Economy", "Premium", "Business", "First Class"]
FLIGHT_CLASSES_CODE = {"Economy": "M", "Premium": "W", "Business": "C", "First Class": "F"}

class FlightSearchApp:
    """
    Class responsible for creating the user interface for the flight search application.
    """

    def __init__(self) -> None:
        """
        Initialize the FlightSearchApp object and load city data.
        Set up the main window and UI containers.
        """
        with open('city_data/city_data.json', 'r') as data_file:
            self.cities = json.load(data_file)

        # Initialize the main window with a specific theme
        self.root = tkk.Window(themename='flatly')
        self.flight_information_container = tkk.Frame()  # Container for flight information input
        self.flight_list_container = tkk.Frame()  # Container for displaying flight results

        # Create UI elements in rows
        self.__create_first_row()
        self.__create_second_row()
        self.__create_third_row()
 
    def __create_first_row(self):
        """Create the first row of UI elements (trip type and flight class)."""
        self.__create_trip_type()
    
    def __create_second_row(self):
        """Create the second row of UI elements (location entries and buttons)."""
        self.location_container = tkk.Frame(self.flight_information_container)
        self.__create_entry()
        self.__create_button()
        self.__create_date_entry()

    def __create_third_row(self):
        """Create the third row of UI elements (listbox for location suggestions)."""
        self.__create_listbox()
    
    def __create_trip_type(self):
        """Create trip type selection (roundtrip or one-way) and flight class dropdown."""
        self.trip_type = tkk.StringVar()
        self.trip_type_container = tkk.Frame(self.flight_information_container)
        
        # Radio buttons for selecting trip type
        roundtrip_radio_button = tkk.Radiobutton(self.trip_type_container,
                                                 text="Roundtrip", 
                                                 value="roundtrip",
                                                 variable=self.trip_type)
        roundtrip_radio_button.grid(row=0, column=0)
        
        oneway_radio_button = tkk.Radiobutton(self.trip_type_container,
                                              text="One-way", 
                                              value="oneway",
                                              variable=self.trip_type)
        oneway_radio_button.grid(row=0, column=1)

        # Dropdown for selecting flight class
        self.flight_classes_dropbox = tkk.Combobox(self.trip_type_container,
                                                   width=9,
                                                   values=FLIGHT_CLASSES,
                                                   state="readonly")
        self.flight_classes_dropbox.current(0)  # Default to "Economy"
        self.flight_classes_dropbox.grid(row=0, column=2)

        # Dropdown for selecting the number of travelers
        travelers_dropbox = tkk.Combobox(self.flight_information_container,
                                         font=("Arial", 22),
                                         width=10,
                                         state='readonly')
        travelers_dropbox.grid(row=1, column=4, padx=10, sticky=tkk.EW, rowspan=2)
        
    def __create_entry(self) -> None:
        """Create entry widgets for origin and destination locations."""
        # Origin location entry with placeholder text
        self.origin_location_entry = tkk.Entry(self.location_container,
                                               font=("Arial", 20),
                                               foreground='grey',
                                               width=16)
        self.origin_location_entry.grid(row=0, column=0, sticky=tkk.EW, padx=5)
        self.origin_location_entry.insert(0, "Enter location...")

        # Destination location entry with placeholder text
        self.destination_location_entry = tkk.Entry(self.location_container,
                                                    font=("Arial", 20),
                                                    foreground='grey',
                                                    width=16)
        self.destination_location_entry.grid(row=0, column=2, sticky=tkk.EW, padx=5)
        self.destination_location_entry.insert(0, "Enter location...")

        # Bind events for location suggestion and validation
        self.origin_location_entry.bind('<KeyRelease>',
                                        lambda event: self.__suggest_entry(event, self.location_suggestion1))
        self.destination_location_entry.bind('<KeyRelease>',
                                             lambda event: self.__suggest_entry(event, self.location_suggestion2))
        
        # Warning labels for empty entries
        self.warning_label1 = tkk.Label(self.location_container, foreground='red', text='Cannot leave empty')
        self.warning_label2 = tkk.Label(self.location_container, foreground='red', text='Cannot leave empty')
        
        # Bind focus events for entry validation and placeholder management
        self.destination_location_entry.bind('<FocusOut>',
                                             lambda event: self.check_entry(event, self.warning_label1))
        self.origin_location_entry.bind('<FocusOut>',
                                        lambda event: self.check_entry(event, self.warning_label2))
        self.origin_location_entry.bind('<FocusIn>', self.delete_placeholder)
        self.destination_location_entry.bind('<FocusIn>', self.delete_placeholder)

    def __create_button(self) -> None:
        """Create buttons for switching locations and searching flights."""
        # Load and resize the exchange symbol image
        img = Image.open("img/exchange_symbol.jpg")
        resized_img = img.resize((50, 50))
        self.exchange_symbol = ImageTk.PhotoImage(resized_img)
         
        # Button for switching origin and destination locations
        self.switch_location_button = tk.Button(self.location_container,
                                                bg='white',
                                                highlightthickness=0,
                                                image=self.exchange_symbol,
                                                command=self._switch)
        self.switch_location_button.grid(row=0, column=1)

        # Search button to trigger flight search
        self.search_button = tk.Button(self.flight_information_container,
                                       text="Search",
                                       height=2,
                                       command=self.search)
        self.search_button.grid(row=1, column=5, rowspan=2, padx=10)
    
    def __create_date_entry(self) -> None:
        """Create date entry widgets for departure and return dates."""
        # Date entry for departure date
        self.departure_date = tkk.DateEntry(self.flight_information_container, dateformat='%d/%m/%Y')
        self.departure_date.grid(row=1, column=3, padx=10, sticky=tkk.EW)

        # Date entry for return date
        self.return_date = tkk.DateEntry(self.flight_information_container, dateformat='%d/%m/%Y')
        self.return_date.grid(row=2, column=3, padx=10, sticky=tkk.EW)

        # Warning label for empty date entries
        self.warning_label3 = tkk.Label(self.location_container, foreground='red', text='Cannot leave empty')
        self.departure_date.bind("<FocusOut>", lambda event: self.check_entry(event, self.warning_label3))

    def __create_listbox(self) -> None:
        """Create listbox widgets for location suggestions."""
        self.selection = tkk.Variable()

        # Listbox for origin location suggestions
        self.location_suggestion1 = tk.Listbox(self.flight_information_container,
                                               height=10,
                                               width=20,
                                               font=('Courier', 15, "bold"))
        self.location_suggestion1.bind('<<ListboxSelect>>',
                                       lambda event: self.__listbox_select(event, self.location_suggestion1, self.origin_location_entry))

        # Listbox for destination location suggestions
        self.location_suggestion2 = tk.Listbox(self.flight_information_container,
                                               height=10,
                                               width=20,
                                               font=('Courier', 15, "bold"))
        self.location_suggestion2.bind('<<ListboxSelect>>',
                                       lambda event: self.__listbox_select(event, self.location_suggestion2, self.destination_location_entry))

    def run(self) -> None:
        """
        Set up and run the main application loop.
        Position UI elements in the window.
        """
        self.trip_type_container.grid(row=0, column=0, columnspan=1, ipadx=40)
        self.location_container.grid(row=1, column=0, columnspan=3, rowspan=2, sticky=tkk.EW)

        # Configure grid layout for responsiveness
        self.location_container.columnconfigure(0, weight=1)
        self.location_container.columnconfigure(2, weight=1)
        self.trip_type_container.columnconfigure(0, weight=1)
        self.trip_type_container.columnconfigure(1, weight=1)
        self.trip_type_container.columnconfigure(2, weight=1)
        self.flight_information_container.columnconfigure(0, weight=1)
        self.flight_information_container.columnconfigure(1, weight=1)
        self.flight_information_container.columnconfigure(2, weight=1)
        self.flight_information_container.columnconfigure(3, weight=1)
        self.flight_information_container.columnconfigure(4, weight=1)

        self.flight_information_container.pack(fill=tkk.BOTH, expand=True)

        # Set window title and size
        self.root.title("Flight Search")
        self.root.geometry('1700x300')
        self.root.mainloop()

    def _switch(self) -> None:
        """Switch the values of origin and destination location entries."""
        location1 = self.origin_location_entry.get()
        location2 = self.destination_location_entry.get()
        self.origin_location_entry.delete(0, tkk.END)
        self.origin_location_entry.insert(0, location2)
        self.destination_location_entry.delete(0, tkk.END)
        self.destination_location_entry.insert(0, location1)

    def __suggest_entry(self, event, listbox) -> None:
        """Suggest location options based on user input in entry widgets."""
        query = event.widget.get().lower()
        results = []

        # Find cities matching the query
        for city in self.cities:
            if query in city['city'].lower():
                results.append(city['city'])
        
        # Display suggestions in the listbox
        listbox.delete(0, tkk.END)
        for city in results[:5]:
            listbox.insert(tkk.END, city)
        listbox.grid(row=1, column=0)
    
    def __listbox_select(self, event, listbox, entry) -> None:
        """Update entry widget with selected suggestion from the listbox."""
        entry.delete(0, tkk.END)
        entry.insert(0, listbox.get(listbox.curselection()))
        listbox.grid_forget()

    def check_entry(self, event, label) -> None:
        """Display a warning if an entry is left empty."""
        if not event.widget.get().strip():
            label.grid(row=2, column=0)
    
    def delete_placeholder(self, event) -> None:
        """Clear placeholder text from the entry widget."""
        entry = event.widget
        if entry.get() == "Enter location...":
            entry.delete(0, tk.END)
            entry.config(foreground='black')
    
    def search(self) -> None:
        """
        Initiate a search for flights based on user input.
        Display search results in the UI.
        """
        data_manager = DataManager()
        flight_search = FlightSearch()
        departure_date = dt.datetime.strptime(self.departure_date.entry.get(), '%d/%m/%Y').date()
        return_date = dt.datetime.strptime(self.return_date.entry.get(), '%d/%m/%Y').date()
        
        # Create a flight data dictionary
        flight_data = {
            'origin': self.origin_location_entry.get(),
            'destination': self.destination_location_entry.get(),
            'departure_date': departure_date,
            'return_date': return_date,
            'trip_type': self.trip_type.get(),
            'class_code': FLIGHT_CLASSES_CODE[self.flight_classes_dropbox.get()],
            'travellers': 1  # Default value, can be customized
        }
        
        # Use DataManager to handle data storage or retrieval (e.g., adding search records)
        data_manager.add_flight_data(flight_data)

        # Execute flight search using FlightSearch class
        results = flight_search.search_flights(flight_data)
        
        # Display the results (currently a placeholder print)
        print(results)


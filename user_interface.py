# This class is responsible for creating the user interface.

import ttkbootstrap as tkk
import tkinter as tk
import json
import datetime as dt
from airport_search import AirportSearch
from flight_search import FlightSearch
from PIL import Image, ImageTk
from data_manager import DataManager                                                                                                                               

FLIGHT_CLASSES = ["Economy","Premium","Business","First Class"]
FLIGHT_CLASSES_CODE = {"Economy":"M","Premium":"W","Business":"C","First Class":"F"}

class FlightSearchApp():
    
    def __init__(self) -> None:
        with open('city_data/city_data.json','r') as data_file:
                self.cities = json.load(data_file)
        self.root = tkk.Window(themename='flatly')
        self.flight_information_container = tkk.Frame()
        self.flight_list_container =tkk.Frame()
        self.__create_first_row()
        self.__create_second_row()
        self.__create_third_row()
 
    def __create_first_row(self):
        self.__create_trip_type()
    
    def __create_second_row(self):
        self.location_container = tkk.Frame(self.flight_information_container)
        self.__create_entry()
        self.__create_button()
        self.__create_date_entry()

    def __create_third_row(self):
        self.__create_listbox()
    
    def __create_trip_type(self):
        self.trip_type = tkk.StringVar()
        
        self.trip_type_container =tkk.Frame(self.flight_information_container)
        roundtrip_radio_button = tkk.Radiobutton(self.trip_type_container,
                                                 text="Roundtrip", 
                                                 value="roundtrip",
                                                 variable=self.trip_type)
        roundtrip_radio_button.grid(row =0,column=0)
        oneway_radio_button = tkk.Radiobutton(self.trip_type_container,
                                              text="One-way", 
                                              value="oneway",
                                              variable=self.trip_type)
        oneway_radio_button.grid(row =0,column=1)
        self.flight_classes_dropbox = tkk.Combobox(self.trip_type_container,
                                      width = 9,
                                      values=FLIGHT_CLASSES,
                                      state="readonly")
        self.flight_classes_dropbox.current(0)
        self.flight_classes_dropbox.grid(row = 0, column= 2)
        travelers_dropbox = tkk.Combobox(self.flight_information_container,
                                 font = ("Arial",22),
                                 width = 10,
                                 state='readonly')
        travelers_dropbox.grid(row=1,column=4,padx = 10,sticky=tkk.EW,rowspan=2)
        
    def __create_entry(self)->None:
         
         self.origin_location_entry = tkk.Entry(self.location_container,
                                                font = ("Arial",20),
                                                foreground='grey',
                                                width = 16)
         self.origin_location_entry.grid(row =0, column= 0,sticky=tkk.EW,padx=5)
         self.origin_location_entry.insert(0,"Enter location...")
         self.destination_location_entry = tkk.Entry(self.location_container,
                                                     font = ("Arial",20),
                                                     foreground='grey',
                                                     width = 16)
         self.destination_location_entry.grid(row =0, column=2,sticky=tkk.EW,padx=5)
         self.destination_location_entry.insert(0,"Enter location...")
         self.origin_location_entry.bind('<KeyRelease>',
                                lambda event :self.__suggest_entry(event,self.location_suggestion1))
         self.destination_location_entry.bind('<KeyRelease>',
                                lambda event :self.__suggest_entry(event,self.location_suggestion2))
         self.warning_label1 = tkk.Label(self.location_container, foreground='red',
                                         text='Cannot leave empty')
         self.warning_label2 = tkk.Label(self.location_container, foreground='red',
                                         text='Cannot leave empty')
         self.destination_location_entry.bind('<FocusOut>',
                                lambda event: self.check_entry(event,self.warning_label1))
         self.origin_location_entry.bind('<FocusOut>',
                                lambda event: self.check_entry(event,self.warning_label2))
         self.origin_location_entry.bind('<FocusIn>',self.delete_placeholder)
         self.destination_location_entry.bind('<FocusIn>',self.delete_placeholder)

    def __create_button(self)->None:
        # Create an image object and resize it
        img = Image.open("img/exchange_symbol.jpg")
        resized_img = img.resize((50,50))
        self.exchange_symbol = ImageTk.PhotoImage(resized_img)
         
        # Button
        self.switch_location_button = tk.Button(self.location_container,
                                            bg = 'white',
                                            highlightthickness=0,
                                            image=self.exchange_symbol,
                                            command=self._switch)
        self.switch_location_button.grid(row=0, column=1)
        self.search_button = tk.Button(self.flight_information_container,
                                text="Search",
                                height= 2,
                                command= self.search,
                                )
        self.search_button.grid(row =1, column= 5,rowspan=2,padx=10)
    
    def __create_date_entry(self) ->None:
        self.departure_date = tkk.DateEntry(self.flight_information_container,dateformat='%d/%m/%Y')
        self.departure_date.grid(row= 1, column=3, padx=10,sticky=tkk.EW )
        self.return_date = tkk.DateEntry(self.flight_information_container,dateformat='%d/%m/%Y')
        self.return_date.grid(row= 2, column=3, padx=10,sticky=tkk.EW )
        self.warning_label3 =self.warning_label1 = tkk.Label(self.location_container, foreground='red',
                                         text='Cannot leave empty')
        self.departure_date.bind("<FocusOut>",
                                       lambda event: self.check_entry(event,self.warning_label3))

    def __create_listbox(self) -> None:
        self.selection = tkk.Variable()
        self.location_suggestion1 = tk.Listbox(self.flight_information_container,
                                                height= 10,
                                                width=20,
                                                font=('Courier',15,"bold"),
                                                )
        self.location_suggestion1.bind('<<ListboxSelect>>',
                            lambda event:self.__listbox_select(event,self.location_suggestion1,self.origin_location_entry))

        self.location_suggestion2 = tk.Listbox(self.flight_information_container,
                                                height= 10,
                                                width=20,
                                                font=('Courier',15,"bold"),
                                                )
        self.location_suggestion2.bind('<<ListboxSelect>>',
                            lambda event:self.__listbox_select(event,self.location_suggestion2,self.destination_location_entry))

    def run(self) -> None:
        self.trip_type_container.grid(row=0, column=0,columnspan=1,ipadx=40)
        self.location_container.grid(row = 1, column=0,columnspan=3,rowspan=2,sticky=tkk.EW)

        self.location_container.columnconfigure(0,weight=1)
        self.location_container.columnconfigure(2,weight=1)
        self.trip_type_container.columnconfigure(0,weight=1)
        self.trip_type_container.columnconfigure(1,weight=1)
        self.trip_type_container.columnconfigure(2,weight=1)
        self.flight_information_container.columnconfigure(0, weight=1)
        self.flight_information_container.columnconfigure(1, weight=1)
        self.flight_information_container.columnconfigure(2, weight=1)
        self.flight_information_container.columnconfigure(3, weight=1)
        self.flight_information_container.columnconfigure(4, weight=1)
        self.flight_information_container.pack(fill=tkk.BOTH, expand =True)

        self.root.title ("Flight Search")
        self.root.geometry('1700x300')
        self.root.mainloop()

    def _switch(self) -> None:
        location1 = self.origin_location_entry.get()
        location2 = self.destination_location_entry.get()
        self.origin_location_entry.delete(0,tkk.END)
        self.origin_location_entry.insert(0,location2)
        self.destination_location_entry.delete(0,tkk.END)
        self.destination_location_entry.insert(0,location1)

    def __suggest_entry(self,event,suggestion) -> None:
        widget = event.widget
        content = widget.get()
        column =widget.grid_info()['column']
        if not self.is_empty(widget):
            cities = self.cities[content[0].upper()]

        if len(content) ==0:
            suggestion.grid_forget()

        elif len(content) == 1:
            suggestion.grid(row =4, column=column)
            for i in range(5):
               suggestion.insert(tkk.END,cities[i])
                                                      
        else:
            suggestion.delete(0, "end")
            for city in cities:
                if suggestion.size() <10 and \
                    content.lower() in city.lower():
                    suggestion.insert(tkk.END,city)

    def __listbox_select(self,event,suggestion,entry) -> None:
        try:
            selected_option = suggestion.get(
                                suggestion.curselection())
            suggestion.grid_forget()
        except:
            pass
        else:
            entry.delete(0,tkk.END)
            entry.insert(tkk.END,selected_option)

    def search(self):
        if self.origin_location_entry.get()=='' or self.destination_location_entry.get() == '' \
        or self.departure_date.entry.get() =='':
            print("Please fill in required information")
        else:
            airport_search = AirportSearch()
            origin_airports =airport_search.search(self.origin_location_entry.get())
            destination_airports = airport_search.search(self.destination_location_entry.get())
            origin_airports = ','.join(origin_airports)
            destination_airports = ','.join(destination_airports)
            flight_search = FlightSearch(origin_airports, destination_airports,
                                        self.departure_date.entry.get(), self.return_date.entry.get(),
                                        FLIGHT_CLASSES_CODE[self.flight_classes_dropbox.get()])
            flights = flight_search.check_flight()
            data_manager = DataManager(flights)
            data_manager.generate()

    def check_entry(self,event,label):
        widget = event.widget
        column = widget.grid_info()['column']
        row = widget.grid_info()['row']
        if not isinstance(widget,tkk.Entry):
            widget = event.widget.entry
            if not widget.get():
                widget.insert(0,"cannot leave empty")
        elif widget.get() =='':
            self.insert_placeholder(widget,"Enter location...")
            label.grid(row = row +1, column =column )
        else:
            label.grid_forget()

    def insert_placeholder(self,widget,text):
        if isinstance(widget, tkk.Entry):
            widget.delete(0,tkk.END)
            widget.config(foreground ='gray')
            widget.insert(0,text)
            widget.icursor(0)

    def delete_placeholder(self,event):
        widget = event.widget
        if widget.get() == "Enter location...":
            widget.delete(0,tkk.END)
            widget.config(foreground = 'black')

    def is_empty(self,event):
        return len(event.get()) == 0
           
            

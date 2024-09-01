# This class is responsible for creating another window for tkinter, and generate the results.

import ttkbootstrap as tkk

class DataManager():
    
    def __init__(self, flights) -> None:
        # Initialize a new Tkinter window (Toplevel) for displaying flight results
        self.sub_root = tkk.Toplevel()
        self.sub_root.title("Flight Results")  
        self.sub_root.geometry("1000x700")  
        self.results = flights  

    def generate(self):
        # Generate labels for each flight result and display them in the new window
        i = 0 
        # Create a label for each flight result
        for flight in self.results:
            label = tkk.Label(self.sub_root, text=flight)
            label.config(border=2, borderwidth=2, relief='raised')  
            label.grid(row=i, column=0) 
            i += 1  

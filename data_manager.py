import ttkbootstrap as tkk

class DataManager():
    
    #This class is responsible for talking to the Google Sheet.
    def __init__(self,flights) -> None:
        self.sub_root = tkk.Toplevel()
        self.sub_root.title("Flight Results")
        self.sub_root.geometry("1000x700")
        self.results = flights

    def generate(self):
        i = 0
        for flight in self.results:
            label = tkk.Label(self.sub_root,text= flight)
            label.config(border= 2, borderwidth=2, relief= 'raised')
            label.grid(row = i, column=0)
            i+= 1
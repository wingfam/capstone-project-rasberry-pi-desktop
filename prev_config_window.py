import customtkinter as ctk
import sqlite3 as sqlite3
from controllers.config_controller import DatabaseController

from views.add_cabinet_screen import AddCabinetScreen
from views.choose_cabinet_screen import ChooseCabinetScreen
from views.config_screen import ConfigScreen
from views.control_screen import ControlScreen
from views.pre_config_screen import PreConfigScreen

class Window(ctk.CTk):
    def __init__(self,  *args, **kwargs):
        ctk.CTk.__init__(self,  *args, **kwargs)
        ctk.CTk.configure(self, fg_color="white")
        self.geometry("1024x600")
        self.title("Pre config window")
        
        self.cabinetName = None
        self.cabinetValues = None
        self.databaseController = DatabaseController(view=self)
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.screen_views = ScreenView().frame_views
        self.frames = self.screen_views
        
        for key, F in self.frames.items():
            frame = F(container, self)
            # the windows class acts as the root window for the frames.
            self.frames[key] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # self.show_frame("PreConfigScreen")
        self.show_frame("ChooseCabinetScreen")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "AddCabinetScreen":
            gotLocationNames = frame.addCabinetController.get_location_data()
            frame.locationNames = gotLocationNames
            frame.after(500, gotLocationNames)

class ScreenView():
    frame_views = {
        # "PreConfigScreen": PreConfigScreen,
        "ChooseCabinetScreen": ChooseCabinetScreen,
        "AddCabinetScreen": AddCabinetScreen,
        "ConfigScreen": ConfigScreen,
        "ControlScreen": ControlScreen,
    }    
  
if __name__ == "__main__":
    root = Window()
    root.mainloop()
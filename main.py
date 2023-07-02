'''
Need to update .venv everytime switch to different enviroment
'''

import customtkinter as ctk
from views.completion_screen import CompletionScreen
from views.instruction_screen import InstructionScreen

from views.main_screen import MainScreen
from views.delivery_screen import DeliveryScreen
from views.pickup_screen import PickupScreen

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("1024x600")
        self.title("Smart Locker")
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.app_data = {}
        
        self.frames = {
            "MainScreen": MainScreen,
            "DeliveryScreen": DeliveryScreen,
            "PickupScreen": PickupScreen,
            "InstructionScreen": InstructionScreen,
            "CompletionScreen": CompletionScreen,
        }
        for key, F in self.frames.items():
            frame = F(container, self)
            # the windows class acts as the root window for the frames.
            self.frames[key] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MainScreen")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        match page_name:
            case "CompletionScreen":
                frame.event_generate("<<GoBackMainScreen>>")
                frame.bind("<<GoBackMainScreen>>", frame.on_show_frame())

if __name__ == "__main__":
    root = MainApp()
    root.mainloop()
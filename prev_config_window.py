import customtkinter as ctk
from views.cabinet_info_screen import CabinetInfoScreen

from views.config_screen import ConfigScreen
from views.control_screen import ControlScreen
from views.pre_config_screen import PreConfigScreen

class Window(ctk.CTk):
    def __init__(self,  *args, **kwargs):
        ctk.CTk.__init__(self,  *args, **kwargs)
        ctk.CTk.configure(self, fg_color="white")
        self.geometry("1024x600")
        self.title("Pre config window")
        
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
        self.show_frame("ConfigScreen")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class ScreenView():
    frame_views = {
        # "PreConfigScreen": PreConfigScreen,
        "ConfigScreen": ConfigScreen,
        "CabinetInfoScreen": CabinetInfoScreen,
        "ControlScreen": ControlScreen,
    }    
  
if __name__ == "__main__":
    root = Window()
    root.mainloop()
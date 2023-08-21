import sys
# import RPi.GPIO as GPIO
import customtkinter as ctk

from controllers.config_controller import DatabaseController, GpioController
from controllers.stream_controller import StreamController
from constants.screen_views import ScreenView


class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("1024x600")
        self.title("Smart Locker")
        
        self.databaseController = DatabaseController(view=self)
        self.gpioController = GpioController(view=self)
        self.streamController = StreamController(view=self)

        self.globalBoxData = {}
        self.globalStreams = {}
        self.app_data = {}
        
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.isRestart = ctk.BooleanVar()
        
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
        
        self.gpioController.setup_box_data()
        self.streamController.set_all_stream()
        
        if not self.globalBoxData:
            print("Need to add cabinet info first")
            self.show_frame("AddCabinetScreen")
        else:
            self.show_frame("MainScreen")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "CompletionScreen":
            frame.event_generate("<<GoBackMainScreen>>")
            frame.bind("<<GoBackMainScreen>>", frame.on_show_frame())
        elif page_name == "ChooseCabinetScreen":
            frame.refresh()
        elif page_name == "AddCabinetScreen":
            frame.set_location_data()
        elif page_name == "EditCabinetScreen":
            frame.editController.get_infos()
        elif page_name == "AddBoxScreen":
            frame.addBoxController.set_cabinetId()
        elif page_name == "ControlScreen":
            frame.cabinetListBox.set_list_box()

    def cleanAndExit(self):
        print("Cleaning...")
        self.streamController.close_all_stream()
        # GPIO.cleanup()
        print("Exiting program...")
        sys.exit()
        

if __name__ == "__main__":
    root = MainApp()
    root.mainloop()
    
    if KeyboardInterrupt or SystemExit:
        root.cleanAndExit()
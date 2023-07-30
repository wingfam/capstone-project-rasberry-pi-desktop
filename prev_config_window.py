import sys
import time
import customtkinter as ctk
import sqlite3 as sqlite3
# import RPi.GPIO as GPIO

from services.firebase_config import firebaseDB
from controllers.config_controller import DatabaseController, GpioController
from controllers.stream_controller import StreamController
from views.add_box_screen import AddBoxScreen
from views.add_cabinet_screen import AddCabinetScreen
from views.choose_cabinet_screen import ChooseCabinetScreen
from views.config_screen import ConfigScreen
from views.control_screen import ControlScreen
from views.edit_cabinet_screen import EditCabinetScreen
from views.pre_config_screen import PreConfigScreen


class MainWindow(ctk.CTk):
    def __init__(self,  *args, **kwargs):
        ctk.CTk.__init__(self,  *args, **kwargs)
        ctk.CTk.configure(self, fg_color="white")
        self.geometry("1024x600")
        self.title("Pre config window")

        self.databaseController = DatabaseController(view=self)
        self.gpioController = GpioController(view=self)
        self.streamController = StreamController(view=self)

        self.globalBoxData = {}
        self.globalStreams = {}
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()

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

        self.gpioController.setup_gpio()
        self.streamController.set_all_stream()
        self.show_frame("ChooseCabinetScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "AddCabinetScreen":
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


class ScreenView():
    frame_views = {
        # "PreConfigScreen": PreConfigScreen,
        "ChooseCabinetScreen": ChooseCabinetScreen,
        "AddCabinetScreen": AddCabinetScreen,
        "ConfigScreen": ConfigScreen,
        "EditCabinetScreen": EditCabinetScreen,
        "AddBoxScreen": AddBoxScreen,
        "ControlScreen": ControlScreen,
    }


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()

    if KeyboardInterrupt or SystemExit:
        root.cleanAndExit()

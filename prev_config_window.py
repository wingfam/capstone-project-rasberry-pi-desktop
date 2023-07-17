import customtkinter as ctk
import sqlite3 as sqlite3
import sys

from urllib.request import pathname2url
from constants.db_table import DbTable, db_file_name
from views.cabinet_info_screen import CabinetInfoScreen
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
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.cabinetId = ""
        self.screen_views = ScreenView().frame_views
        self.frames = self.screen_views
        
        for key, F in self.frames.items():
            frame = F(container, self)
            # the windows class acts as the root window for the frames.
            self.frames[key] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.conn = self.opendb(db_file_name)
        
        if self.conn:
            self.conn.close()
        else:
            print("Create new database")
            self.create_new_db(self.conn)
        
        # self.show_frame("PreConfigScreen")
        self.show_frame("ChooseCabinetScreen")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "ConfigScreen":
            print(self.cabinetId)
        elif page_name == "CabinetInfoScreen":
            cabinetId = self.cabinetId
            frame.get_box_by_cabinetId(cabinetId)
            frame.get_all_location_name()
        
    def opendb(self, db_file_name):
        conn = None
        try:
            # Making a connection between sqlite3 database and Python Program
            dburi = 'file:{}?mode=rw'.format(pathname2url(db_file_name))
            conn = sqlite3.connect(dburi, uri=True)
        except sqlite3.OperationalError:
            print( "Database doesn't exist.\n")
            return False
        
        return conn
                
    def create_new_db(self, conn):
        tables = DbTable()
        try:
            conn = sqlite3.connect(db_file_name)
            cursor = conn.cursor()
            # Create new table
            for table in tables.tableList:
                cursor.execute(table)
                
        except sqlite3.DatabaseError as e:
            print(e)
        finally:
            conn.close()
            
        print("New database has been created.")
        

class ScreenView():
    frame_views = {
        # "PreConfigScreen": PreConfigScreen,
        "ChooseCabinetScreen": ChooseCabinetScreen,
        "ConfigScreen": ConfigScreen,
        "CabinetInfoScreen": CabinetInfoScreen,
        "ControlScreen": ControlScreen,
    }    
  
if __name__ == "__main__":
    root = Window()
    root.mainloop()
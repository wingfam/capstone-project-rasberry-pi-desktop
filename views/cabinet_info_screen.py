import customtkinter as ctk
import sqlite3 as sqlite3
from customtkinter import StringVar, CTkButton, CTkLabel, CTkEntry, CTkComboBox, CENTER
from constants.image_imports import back_image
from tkintertable import TableCanvas, TableModel
from constants.db_table import db_file_name
from services.auth import firebase_login
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory

class CabinetInfoScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        
        label_font = ctk.CTkFont(size=24)
        
        self.name = StringVar()
        self.createDate = StringVar()
        self.statusVar = StringVar()
        self.locationVar = StringVar()
        
        self.statusValues = ["Yes", "No"]
        self.locationNames = []
        self.boxData = {}
        
        CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=lambda: self.controller.show_frame("ConfigScreen"),
        ).place(relx=.05, rely=.10, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="Box list: ",
        ).place(relx=.60, rely=.08, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Cabinet name: ",
        ).place(relx=.08, rely=.25, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Create Date: ",
        ).place(relx=.08, rely=.35, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Is Available: ",
        ).place(relx=.08, rely=.45, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Location: ",
        ).place(relx=.08, rely=.55, anchor=CENTER)
        
        self.name_entry = CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=label_font,
            textvariable=self.name,
        )
        self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=CENTER)
        
        self.create_date_entry = CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=label_font,
            textvariable=self.createDate,
        )
        self.create_date_entry.place(relwidth=.23, relx=.31, rely=.35, anchor=CENTER)
        
        self.status_combobox = CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            font=label_font,
            state="readonly",
            values=self.statusValues,
            variable=self.statusVar,
            command=self.status_combobox_callback
        )
        self.status_combobox.place(relwidth=.23, relx=.31, rely=.45, anchor=CENTER)
        
        self.location_combobox = CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            state="readonly",
            font=label_font,
            values=self.locationNames,
            variable=self.locationVar,
            command=self.location_combobox_callback
        )
        self.location_combobox.place(relwidth=.23, relx=.310, rely=.55, anchor=CENTER)
        
        CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Update",
            command=lambda: self.update_info()
        ).place(relwidth=.2, relx=.12, rely=.72, anchor=ctk.CENTER)
        
        CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Reload",
            command=lambda: self.reload_info()
        ).place(relwidth=.2, relx=.35, rely=.72, anchor=ctk.CENTER)
        
        self.boxTable = BoxList(self, controller=self.controller)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=CENTER)
        
    def status_combobox_callback(self, choice):
        self.statusVar.set(choice)
        print("status_combobox:", self.statusVar.get())
    
    def location_combobox_callback(self, choice):
        self.locationVar.set(choice)
        print("location_combobox:", self.locationVar.get())
    
    def update_info(self):
        print("File has been save!")
        tableModel = self.boxTable.table.getModel()
        records = tableModel.data
        for record in records.values():
            print(record)
    
    def reload_info(self):
        print("Reloaded!")
        
    def get_all_location_name(self):
        try:
            fb_login = firebase_login()
            fb_locations = firebaseDB.child("Location").get(fb_login["idToken"])
            for location in fb_locations.each():
                location_name = location.val()['name']
                self.locationNames.append(location_name)
        except IndexError:
            print("Location doesn't exist")
            
        print("Location names loaded")
        self.location_combobox.configure(require_redraw=True, values=self.locationNames)
    
    def get_box_by_cabinetId(self, cabinetId):
        conn = self.controller.opendb(db_file_name)
        newData = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * From Box WHERE cabinetId = ?", (cabinetId))
            
            count = 0
            for row in results:
                data = {
                    count: row
                }
                newData.update(data)
                count += 1
                
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        # TODO: add newData to data table
        self.boxTable.data = newData
        self.boxTable.table.redraw()

class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        
        self.data = {}
        
        self.table = TableCanvas(
            parent=self, 
            data=self.data,
			cellwidth=83, 
            cellbackgr='#e3f698',
			thefont=('Arial', 12),
            rowheight=24, 
            rowheaderwidth=30,
            read_only=False,
        )
        
        self.table.show()
            
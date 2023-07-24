import customtkinter as ctk

from tkinter import IntVar
from constants.image_imports import back_image
from tkintertable import TableCanvas
from controllers.config_controller import DatabaseController
from controllers.stream_controller import StreamController

class EditCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.parent = parent
        self.controller = controller
        
        self.databaseController = DatabaseController(view=self)
        self.streamController = StreamController(view=self)
        
        self.statusComboboxValues = ["Yes", "No"]
        self.locationComboboxValues = []
        self.locationData = {}
        self.boxData = {}
        
        self.statusComboboxVar = ctk.StringVar()
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.isAvailable = IntVar()
        self.cabinetLocation = ctk.StringVar()
        self.locationId = ctk.StringVar()
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=self.go_back_prev_screen,
        ).place(relx=.05, rely=.10, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Box list: ",
        ).place(relx=.60, rely=.08, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Cabinet name: ",
        ).place(relx=.08, rely=.25, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Is Available: ",
        ).place(relx=.08, rely=.35, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Location: ",
        ).place(relx=.08, rely=.45, anchor=ctk.CENTER)
        
        self.error_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text_color="red",
            text="",
        )
        self.error_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        
        self.name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=ctk.CTkFont(size=24),
            textvariable=self.cabinetName,
        )
        self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=ctk.CENTER)
        
        self.status_combobox = ctk.CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            font=ctk.CTkFont(size=24),
            state="readonly",
            values=self.statusComboboxValues,
            variable=self.statusComboboxVar,
            command=self.status_combobox_callback
        )
        self.status_combobox.place(relwidth=.23, relx=.31, rely=.35, anchor=ctk.CENTER)
        
        self.location_combobox = ctk.CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            state="readonly",
            font=ctk.CTkFont(size=16),
            values=self.locationComboboxValues,
            variable=self.cabinetLocation,
            command=self.location_combobox_callback
        )
        self.location_combobox.place(relwidth=.23, relx=.310, rely=.45, anchor=ctk.CENTER)
    
        ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Upload",
            # command=self.refresh
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.62, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Update",
            command=self.update_data
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.75, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Refresh",
            command=self.refresh
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.88, anchor=ctk.CENTER)
        
        self.boxTable = BoxList(self, controller=self.controller)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
         
    def status_combobox_callback(self, choice):
        if choice == 'Yes':
            self.isAvailable.set(1)
        elif choice == 'No':
            self.isAvailable.set(0)
        self.statusComboboxVar.set(choice)
        choice = self.statusComboboxVar.get()
        print("status_combobox:", choice)
    
    def location_combobox_callback(self, choice):
        self.cabinetLocation.set(choice)
        locationChoice = self.cabinetLocation.get()
        for value in self.locationData.items():
            if value[1]['locationName'] == locationChoice:
                self.locationId.set(value[1]['locationId'])
        print("location_combobox:", locationChoice)

    def set_location_data(self):
        results = self.databaseController.get_location_data()
        self.locationData.update(results)
        
        for key, value in self.locationData.items():
            self.locationComboboxValues.append(value['locationName'])
        
        self.location_combobox.configure(values=self.locationComboboxValues)
    
    def get_infos(self):
        cabinetInfos = self.databaseController.get_cabinet_by_name(
            self.controller.cabinetName.get())
        
        self.cabinetId.set(cabinetInfos['id'])
        self.cabinetName.set(cabinetInfos['name'])
        self.isAvailable.set(cabinetInfos['isAvailable'])
        
        if cabinetInfos['isAvailable'] == 0:
            self.statusComboboxVar.set('No')
        elif cabinetInfos['isAvailable'] == 1:
            self.statusComboboxVar.set('Yes')
        
        self.set_location_data()
        for key, value in self.locationData.items():
            if value['locationId'] == cabinetInfos['locationId']:
                self.cabinetLocation.set(value['locationName'])
        
        boxResults = self.databaseController.get_box_by_cabinetId(self.cabinetId.get())
        model = self.boxTable.table.model
        model.importDict(boxResults)
        self.boxTable.data.update(boxResults)
        self.boxTable.table.redraw()
    
    def update_data(self):
        cabinetValue = {
           'name': self.cabinetName.get(),
           'isAvailable': self.isAvailable.get(),
           'locationId': self.locationId.get(),
           'id': self.cabinetId.get()
        }
        
        self.controller.cabinetName.set(cabinetValue['name'])
        self.databaseController.update_cabinet(cabinetValue)
        
        boxTableData = self.boxTable.table.getModel().data
        for key, value in boxTableData.items():
            self.databaseController.update_box(value)
    
    def refresh(self):
        self.locationData.clear()
        self.locationComboboxValues.clear()
        self.get_infos()
    
    def go_back_prev_screen(self):
        self.refresh()
        self.controller.show_frame("ConfigScreen")
   
class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        self.parent = parent
        
        self.data = {}
        
        self.table = TableCanvas(
            parent=self,
            data=self.data,
			cellwidth=130,
            cellbackgr='#e3f698',
			thefont=('Arial', 12),
            rowheight=24, 
            rowheaderwidth=30,
            read_only=False,
        )
        
        self.table.show()
            
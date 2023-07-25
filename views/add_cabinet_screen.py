import customtkinter as ctk

from tkinter import IntVar
from constants.image_imports import back_image
from tkintertable import TableCanvas
from controllers.config_controller import AddCabinetController, DatabaseController
from controllers.stream_controller import StreamController


class AddCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.parent = parent
        self.controller = controller
        self.databaseController = DatabaseController(view=self)
        self.addCabinetController = AddCabinetController(view=self)
        self.streamController = StreamController(view=self)
        
        self.statusComboboxValues = ["Yes", "No"]
        self.locationComboboxValues = []
        self.locationData = {}
        
        self.statusComboboxVar = ctk.StringVar()
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.cabinetIsAvailable = IntVar()
        self.cabinetLocation = ctk.StringVar()
        self.locationId = ctk.StringVar()
        
        label_font = ctk.CTkFont(size=24)
        
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
            font=label_font,
            text="Box list: ",
        ).place(relx=.60, rely=.08, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Cabinet name: ",
        ).place(relx=.08, rely=.25, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Is Available: ",
        ).place(relx=.08, rely=.35, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Location: ",
        ).place(relx=.08, rely=.45, anchor=ctk.CENTER)
        
        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text_color="red",
            text="",
        )
        self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        
        self.name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=label_font,
            textvariable=self.cabinetName,
        )
        self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=ctk.CENTER)
        
        self.status_combobox = ctk.CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            font=label_font,
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
            font=label_font,
            variable=self.cabinetLocation,
            command=self.location_combobox_callback
        )
        self.location_combobox.place(relwidth=.23, relx=.310, rely=.45, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="1. Save data",
            command=self.save_data
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.62, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="2. Upload data",
            command=self.upload_data
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.75, anchor=ctk.CENTER)
        
        self.boxTable = BoxList(self, controller=self.controller)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
    
    def save_data(self):
        self.addCabinetController.save_to_database()
    
    def upload_data(self):
        isCabinetUpload = self.addCabinetController.upload_cabinet()
        isCodeUpload = self.addCabinetController.upload_mastercode(self.cabinetId)
        isBoxUpload = self.addCabinetController.upload_box(self.cabinetId)
        if isCabinetUpload and isCodeUpload and isBoxUpload:
            self.streamController.set_cabinet_stream(self.cabinetId.get())
            self.streamController.set_box_stream(self.cabinetId.get())
            self.streamController.set_mastercode_stream(self.cabinetId.get())
            self.display_label.configure(text_color="green", text="New cabinet uploaded")
    
    def set_location_data(self):
        results = self.databaseController.get_location_data()
        self.locationData.update(results)
        for key, value in self.locationData.items():
            self.locationComboboxValues.append(value['locationName'])
            
        datalist = self.locationComboboxValues
        return self.location_combobox.configure(require_redraw=True, values=datalist,)

    def refresh(self):
        self.locationComboboxValues = []
        
        self.cabinetName.set("")
        self.statusComboboxVar.set("")
        self.cabinetLocation.set("")
        self.display_label.configure(text="")
    
    def go_back_prev_screen(self):
        self.refresh()
        self.controller.show_frame("ChooseCabinetScreen")
        
    def status_combobox_callback(self, choice):
        if choice == 'Yes':
            self.cabinetIsAvailable.set(1)
        elif choice == 'No':
            self.cabinetIsAvailable.set(0)
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


class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        self.parent = parent
        
        self.data = {
            'rec': {
                'nameBox': "",
                'size': "",
                'width': 0,
                'height': 0,
                'solenoidGpio': 0,
                'switchGpio': 0,
                'loadcellDout': 0,
                'loadcellSck': 0,
            }
        }
        
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
            
import customtkinter as ctk

from tkinter import IntVar
from constants.image_imports import back_image
from tkintertable import TableCanvas
from controllers.config_controller import AddCabinetController, DatabaseController
from controllers.stream_controller import StreamController


class AddCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.parent = parent
        self.root = root
        self.databaseController = DatabaseController(view=self)
        self.addCabinetController = AddCabinetController(view=self)
        self.streamController = StreamController(view=self)
        
        self.statusComboboxValues = ["Yes", "No"]
        self.locationComboboxValues = []
        self.locationData = {}
        
        self.statusComboboxVar = ctk.StringVar()
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.cabinetStatus = IntVar()
        self.cabinetLocation = ctk.StringVar()
        self.businessId = ctk.StringVar()
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
        
        self.name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=label_font,
            textvariable=self.cabinetName,
        )
        
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
        
        self.save_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="1. Save data",
            command=self.save_data
        )
        
        self.upload_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="2. Upload data",
            state=ctk.DISABLED,
            command=self.upload_data
        )
        
        self.boxTable = BoxList(self, root=self.root)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
        self.location_combobox.place(relwidth=.23, relx=.310, rely=.45, anchor=ctk.CENTER)
        self.status_combobox.place(relwidth=.23, relx=.31, rely=.35, anchor=ctk.CENTER)
        self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=ctk.CENTER)
        self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        self.save_button.place(relwidth=.35, relheight=.10, relx=.22, rely=.62, anchor=ctk.CENTER)
        self.upload_button.place(relwidth=.35, relheight=.10, relx=.22, rely=.75, anchor=ctk.CENTER)
    
    def save_data(self):
        self.upload_button.configure(state=ctk.NORMAL)
        self.addCabinetController.save_to_database()
    
    def upload_data(self):
        self.upload_button.configure(state=ctk.DISABLED)
        self.addCabinetController.upload_to_firebase()
    
    def set_location_data(self):
        results = self.databaseController.get_location_data()
        self.locationData.update(results)
        
        for key, value in self.locationData.items():
            self.locationComboboxValues.append(value['locationName'])
        
        return self.location_combobox.configure(require_redraw=True, values=self.locationComboboxValues,)

    def refresh(self):
        self.locationData.clear()
        self.locationComboboxValues.clear()
        self.cabinetName.set("")
        self.statusComboboxVar.set("")
        self.cabinetLocation.set("")
        self.display_label.configure(text="")
        self.location_combobox.set('')
        
    def go_back_prev_screen(self):
        self.refresh()
        self.root.show_frame("ChooseCabinetScreen")
        
    def status_combobox_callback(self, choice):
        if choice == 'Yes':
            self.cabinetStatus.set(1)
        elif choice == 'No':
            self.cabinetStatus.set(0)
        self.statusComboboxVar.set(choice)
        choice = self.statusComboboxVar.get()
    
    def location_combobox_callback(self, choice):
        self.cabinetLocation.set(choice)
        locationChoice = self.cabinetLocation.get()
        for key, value in self.locationData.items():
            if value['locationName'] == locationChoice:
                self.businessId.set(value['businessId'])
                self.locationId.set(value['locationId'])
        # print(locationChoice)
        # print("BussinesId: ", self.businessId.get())
        # print("LocationId: ", self.locationId.get())


class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.root = root
        self.parent = parent
        
        self.data = {
            'rec': {
                'nameBox': "",
                'solenoidGpio': 0,
                'switchGpio': 0,
                'loadcellDout': 0,
                'loadcellSck': 0,
                'loadcellRf': 0,
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
            
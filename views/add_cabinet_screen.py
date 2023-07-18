import customtkinter as ctk
from customtkinter import StringVar, CTkButton, CTkLabel, CTkEntry, CTkComboBox, CENTER
from constants.image_imports import back_image
from tkintertable import TableCanvas
from controllers.config_controller import AddCabinetController

class AddCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        self.addCabinetController = AddCabinetController(view=self)
        
        label_font = ctk.CTkFont(size=24)
        
        self.statusValues = ["Yes", "No"]
        self.locationNames = []
        self.locationData = {}
        self.boxData = {}
        
        self.cabinetName = StringVar()
        self.cabinetIsAvailable = StringVar()
        self.cabinetLocation = StringVar()
        self.locationId = StringVar()
        
        CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=lambda: self.reset(),
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
            text="Is Available: ",
        ).place(relx=.08, rely=.35, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Location: ",
        ).place(relx=.08, rely=.45, anchor=CENTER)
        
        self.name_entry = CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=label_font,
            textvariable=self.cabinetName,
        )
        self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=CENTER)
        
        self.status_combobox = CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            font=label_font,
            state="readonly",
            values=self.statusValues,
            variable=self.cabinetIsAvailable,
            command=self.status_combobox_callback
        )
        self.status_combobox.place(relwidth=.23, relx=.31, rely=.35, anchor=CENTER)
        
        self.location_combobox = CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            state="readonly",
            font=label_font,
            values=self.locationNames,
            variable=self.cabinetLocation,
            command=self.location_combobox_callback
        )
        self.location_combobox.place(relwidth=.23, relx=.310, rely=.45, anchor=CENTER)
        
        CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Upload to Firebase",
            command=lambda: self.addCabinetController.upload_to_firebase()
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.62, anchor=ctk.CENTER)
        
        CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Save to Database",
            command=lambda: self.addCabinetController.save_to_database()
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.75, anchor=ctk.CENTER)
        
        self.boxTable = BoxList(self, controller=self.controller)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=CENTER)
    
    def reset(self):
        self.locationNames = []
        self.boxData = {}
        
        self.cabinetName.set("")
        self.cabinetIsAvailable.set("")
        self.cabinetLocation.set("")
        
        self.controller.show_frame("ChooseCabinetScreen")
        
    def status_combobox_callback(self, choice):
        self.cabinetIsAvailable.set(choice)
        choice = self.cabinetIsAvailable.get()
        print("status_combobox:", choice)
    
    def location_combobox_callback(self, choice):
        self.cabinetLocation.set(choice)
        locationName = self.cabinetLocation.get()
        for value in self.locationData.items():
            if value['locationName'] == locationName:
                self.locationId.set(value['locationId'])
        print("location_combobox:", locationName)


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
                'width': "",
                'height': "",
                'solenoidGpio': "",
                'switchGpio': "",
                'loadcellDout': "",
                'loadcellSck': "",
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
            
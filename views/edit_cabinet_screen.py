import time
import customtkinter as ctk

from tkinter import IntVar
from constants.image_imports import back_image, refresh_image
from tkintertable import TableCanvas
from controllers.config_controller import DatabaseController, EditCabinetController
from controllers.stream_controller import StreamController

class EditCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.parent = parent
        self.root = root
        
        self.editController = EditCabinetController(view=self)
        self.databaseController = DatabaseController(view=self)
        self.streamController = StreamController(view=self.root)
        
        self.statusComboboxValues = ["Yes", "No"]
        self.locationComboboxValues = []
        self.locationData = {}
        self.cabinetData = {}
        
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
            command=self.go_back,
        ).place(relx=.05, rely=.10, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=refresh_image,
            command=self.reload,
        ).place(relx=.90, rely=.05, anchor=ctk.CENTER)
        
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
        
        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text="",
        )
        self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        
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
            text="Save data",
            command=self.update
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.62, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Reupload",
            command=self.reupload
        ).place(relwidth=.35, relheight=.10, relx=.22, rely=.75, anchor=ctk.CENTER)
        
        self.boxTable = BoxList(self, root=self.root)
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
        self.set_location_id(self.cabinetLocation.get())
    
    def update(self):
        self.editController.update_data()
        self.reload()
        self.display_label.configure(text_color='green', text='Update successful')
        
    def reupload(self):
        isCabinetUpload = self.editController.reupload_cabinet()
        isBoxUpload = self.editController.reupload_box()
        if isBoxUpload and isCabinetUpload:
            self.display_label.configure(text_color='green', text='Upload successful')
        else:
            self.display_label.configure(text_color='red', text='Upload unsuccessful')
    
    def reload(self):
        self.locationData.clear()
        self.locationComboboxValues.clear()
        self.editController.get_infos()
        
    def go_back(self):
        # Clear display label
        self.display_label.configure(text='') 
        self.boxTable.data.clear()
        
        # Clear data inside table
        tableData = self.boxTable.table.getModel().data
        tableData.clear()
        
        self.root.show_frame("ConfigScreen")
   
class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.root = root
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
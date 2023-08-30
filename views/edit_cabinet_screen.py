import datetime
import customtkinter as ctk

from tkinter import IntVar
from constants.image_imports import back_image, add_image
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
        self.boxData = {}
        
        self.statusComboboxVar = ctk.StringVar()
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.masterCode = ctk.StringVar()
        self.status = IntVar()
        self.cabinetLocation = ctk.StringVar()
        self.businessId = ctk.StringVar()
        self.locationId = ctk.StringVar()
        
        self.go_back_btn = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=self.go_back,
        )
        
        self.add_box_btn = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text="",
            image=add_image,
            command=self.go_to_add_box_screen
        )

        self.box_list_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Box list: ",
        )
        
        self.cabinet_name_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Cabinet name: ",
        )
        
        self.status_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Is Available: ",
        )
        
        self.location_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Location: ",
        )
        
        # self.master_code_label = ctk.CTkLabel(
        #     master=self,
        #     width=200,
        #     anchor="e",
        #     text_color="black",
        #     font=ctk.CTkFont(size=24),
        #     text="Master Code: ",
        # )
        
        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text="",
        )
        
        self.name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=ctk.CTkFont(size=24),
            textvariable=self.cabinetName,
        )
        
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
    
        # self.master_code_entry = ctk.CTkEntry(
        #     master=self,
        #     width=200,
        #     fg_color="white",
        #     text_color="black",
        #     font=ctk.CTkFont(size=24),
        #     textvariable=self.masterCode,
        # )
        
        self.save_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Update Data",
            command=self.update
        )
        
        self.boxTable = BoxList(self, root=self.root)
        
        
        self.go_back_btn.place(relx=.05, rely=.10, anchor=ctk.CENTER)
        self.add_box_btn.place(relx=.80, rely=.05, anchor=ctk.CENTER)
        self.box_list_label.place(relx=.60, rely=.08, anchor=ctk.CENTER)
        self.cabinet_name_label.place(relx=.08, rely=.25, anchor=ctk.CENTER)
        self.status_label.place(relx=.08, rely=.35, anchor=ctk.CENTER)
        self.location_label.place(relx=.08, rely=.45, anchor=ctk.CENTER)
        # self.master_code_label.place(relx=.08, rely=.55, anchor=ctk.CENTER)
        self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=ctk.CENTER)
        self.status_combobox.place(relwidth=.23, relx=.31, rely=.35, anchor=ctk.CENTER)
        self.location_combobox.place(relwidth=.23, relx=.31, rely=.45, anchor=ctk.CENTER)
        # self.master_code_entry.place(relwidth=.23, relx=.31, rely=.55, anchor=ctk.CENTER)
        self.save_button.place(relwidth=.25, relheight=.10, relx=.70, rely=.85, anchor=ctk.CENTER)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
         
    def status_combobox_callback(self, choice):
        if choice == 'Yes':
            self.status.set(1)
        elif choice == 'No':
            self.status.set(0)
            
        self.statusComboboxVar.set(choice)
        choice = self.statusComboboxVar.get()
        
        for box in self.boxData.values():
            if self.status.get():
                box['status'] = 1
            else:
                box['status'] = 0
            
        print("Box " + box['nameBox'] + " status is: ", box['status'])
            
    
    def location_combobox_callback(self, choice):
        self.cabinetLocation.set(choice)
        locationChoice = self.cabinetLocation.get()
        for key, value in self.locationData.items():
            if value['locationName'] == locationChoice:
                self.businessId.set(value['businessId'])
                self.locationId.set(value['locationId'])
    
    def update(self):
        isCabinetUpdate = self.editController.update_cabinet_data()
        isBoxUpdate = self.editController.update_box_data()
        isLogUpdate = self.editController.save_cabinet_log()
        
        isCabinetUpload = self.editController.reupload_cabinet()
        isBoxUpload = self.editController.reupload_box()
        isLogUpload = self.editController.upload_cabinetLog(self.cabinetId.get())
        
        if isCabinetUpdate and isBoxUpdate and isLogUpdate and isCabinetUpload and isBoxUpload and isLogUpload:
            self.root.isRestart.set(True)
            self.root.cabinetName.set(self.cabinetName.get())
            self.display_label.configure(text_color='green', text='Update successful')
        else:
            self.display_label.configure(text_color='red', text='Update unsuccessful')
    
    def refresh(self):
        self.locationData.clear()
        self.locationComboboxValues.clear()
        self.cabinetName.set("")
        self.statusComboboxVar.set("")
        self.location_combobox.set("")
        self.display_label.configure(text="") 
        self.boxTable.data.clear()
        tableData = self.boxTable.table.getModel().data
        tableData.clear()
    
    def go_to_add_box_screen(self):
        self.root.show_frame("AddBoxScreen")
       
    def go_back(self):
        self.refresh()
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
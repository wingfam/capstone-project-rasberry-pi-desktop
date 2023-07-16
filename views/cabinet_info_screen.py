import customtkinter as ctk
from customtkinter import StringVar, CTkButton, CTkLabel, CTkEntry, CTkComboBox, CENTER
from constants.image_imports import back_image
from tkintertable import TableCanvas, TableModel

class CabinetInfoScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        
        label_font = ctk.CTkFont(size=24)
        
        self.name = StringVar()
        self.createDate = StringVar()
        self.status_var = StringVar()
        self.location_var = StringVar()
        
        self.status_values = ["Yes", "No"]
        self.location_values = ["Vinhomes Grand Park", "Thủ Thiêm Garden"]
        
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
        ).place(relx=.08, rely=.30, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Create Date: ",
        ).place(relx=.08, rely=.40, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Is Available: ",
        ).place(relx=.08, rely=.50, anchor=CENTER)
        
        CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Location: ",
        ).place(relx=.08, rely=.60, anchor=CENTER)
        
        self.name_entry = CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=label_font,
            textvariable=self.name,
        )
        self.name_entry.place(relx=.31, rely=.30, anchor=CENTER)
        
        self.create_date_entry = CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=label_font,
            textvariable=self.createDate,
        )
        self.create_date_entry.place(relx=.31, rely=.40, anchor=CENTER)
        
        self.status_combobox = CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            font=label_font,
            state="readonly",
            values=self.status_values,
            variable=self.status_var,
            command=self.status_combobox_callback
        )
        self.status_combobox.place(relwidth=.2, relx=.31, rely=.50, anchor=CENTER)
        
        self.location_combobox = CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            state="readonly",
            font=label_font,
            values=self.location_values,
            variable=self.location_var,
            command=self.location_combobox_callback
        )
        self.location_combobox.place(relwidth=.23, relx=.322, rely=.60, anchor=CENTER)
        
        self.boxList = BoxList(self, controller=self.controller)
        self.boxList.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=CENTER)
    
    def status_combobox_callback(self, choice):
        self.status_var.set(choice)
        print("status_combobox:", self.status_var.get())
    
    def location_combobox_callback(self, choice):
        self.location_var.set(choice)
        print("location_combobox:", self.location_var.get())

class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        
        data = {
            'rec1': {
                'Name': '01', 
                'Size': 'S', 
                'Width': 420,
                'Height': 420,
                'Status': 'available',
                'isStore': 'no'
            },
            'rec2': {
                'Name': '02', 
                'Size': 'M', 
                'Width': 520,
                'Height': 520,
                'Status': 'available',
                'isStore': 'no'
            }
        } 
        
        model = TableModel()
        
        table = TableCanvas(
            self, 
            data=data,
			cellwidth=83, 
            cellbackgr='#e3f698',
			thefont=('Arial', 12),
            rowheight=24, 
            rowheaderwidth=30,
            read_only=True,
        )
        
        table.show()
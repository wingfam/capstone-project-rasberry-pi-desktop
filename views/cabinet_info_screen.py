import customtkinter as ctk
import tkinter as tk
from tkintertable import TableCanvas, TableModel

class CabinetInfo(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        
        label_font = ctk.CTkFont(size=24)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="Cabinet name: ",
        ).place(relx=.13, rely=.30, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="Location: ",
        ).place(relx=.13, rely=.40, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="Status: ",
        ).place(relx=.13, rely=.50, anchor=ctk.CENTER)
        
        ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="Create Date: ",
        ).place(relx=.13, rely=.60, anchor=ctk.CENTER)
        
        self.name_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="cabinetName",
        ).place(relx=.33, rely=.30, anchor=ctk.CENTER)
        
        self.location_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="locationName",
        ).place(relx=.33, rely=.40, anchor=ctk.CENTER)
        
        self.status_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="cabinetStatus",
        ).place(relx=.33, rely=.50, anchor=ctk.CENTER)
        
        self.create_date_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="cabinetCreateDate",
        ).place(relx=.33, rely=.60, anchor=ctk.CENTER)
        
        self.boxList = BoxList(self, controller=self.controller)
        self.boxList.place(relwidth=.5, relheight=.65, relx=.70, rely=.45, anchor=ctk.CENTER)

class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.controller = controller
        
        data = {
            'rec1': {
                'Name': '02', 
                'Size': 'S', 
                'Width': 420,
                'Height': 420,
                'Status': 'available',
                'isStore': 'not'
            },
            'rec2': {
                'Name': '01', 
                'Size': 'M', 
                'Width': 520,
                'Height': 520,
                'Status': 'available',
                'isStore': 'not'
            }
        } 
        
        model = TableModel()
        
        table = TableCanvas(
            self, 
            data=data,
			cellwidth=80, 
            cellbackgr='#e3f698',
			thefont=('Arial', 12),
            rowheight=24, 
            rowheaderwidth=30,
            read_only=True,
        )
        
        table.show()
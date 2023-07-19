from tkinter import StringVar
import customtkinter as ctk
from constants.image_imports import home_image, add_image, refresh_image
from controllers.config_controller import ChooseCabinetController
from CTkListbox import *
'''TODO: Thêm stream cho mỗi cabinet để khi cập nhật trên firebase, update lại local database'''
class ChooseCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.controller = controller
        self.cabinetController = ChooseCabinetController(view=self)
        self.chooseCabinet = StringVar()
        
        button_font = ctk.CTkFont(size=30, weight="bold")
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=home_image,
            command=lambda: self.go_back_main_screen(),
        ).place(relx=.10, rely=.10, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Add cabinet",
            command=lambda: self.go_to_add_screen(),
        ).place(relwidth=.25, relheight=.10, relx=.35, rely=.32, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Check cabinet",
            command=lambda: self.check_cabinet()
        ).place(relwidth=.25, relheight=.10, relx=.35, rely=.47, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Reload",
        ).place(relwidth=.25, relheight=.10, relx=.35, rely=.62, anchor=ctk.CENTER)
        
        self.error_label = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=18),
            text_color="red",
            text="",
        )
        self.error_label.place(rely=.15, relx=.795, anchor="e")
        
        self.cabinetButtonFrame = CabinetListFrame(self)
        self.cabinetButtonFrame.place(rely=.45, relx=.75, anchor=ctk.CENTER)
        
    def set_cabinet_name(self, selected_option):
        self.controller.cabinetId = selected_option
    
    def check_cabinet(self):
        if not self.controller.cabinetName:
            self.error_label.configure(text="Please choose a cabinet")
    
    def go_back_main_screen(self):
        self.refresh()
        self.controller.show_frame("MainScreen")
    
    def go_to_add_screen(self):
        self.refresh()
        self.controller.show_frame("AddCabinetScreen")
    
    def refresh(self):
        self.error_label.configure(text="")

class CabinetListFrame(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.parent = parent
        
        cabinets = self.parent.cabinetController.get_all_cabinet()
        
        self.cabinetListBox = CTkListbox(
            self, 
            width=280, 
            height=280,
            font=ctk.CTkFont(size=24),
            text_color='black',
            command=self.parent.set_cabinet_name
        )
        self.cabinetListBox .pack()
        
        self.get_cabinet_name(cabinets)
    
    def setCabinetId(self, cabinetId, cabinetValues):
        self.parent.controller.cabinetId = cabinetId
        self.parent.controller.cabinetValues = cabinetValues
        self.parent.controller.show_frame("ConfigScreen")
    
    def get_cabinet_name(self, cabinets):
        for key, value in cabinets.items():
            self.cabinetListBox.insert(key, value['nameCabinet'])
    
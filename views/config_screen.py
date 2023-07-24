import customtkinter as ctk

from customtkinter import StringVar
from constants.image_imports import back_image
from controllers.config_controller import DatabaseController, EditCabinetController
from views.edit_cabinet_screen import EditCabinetScreen

class ConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.controller = controller
        self.databaseController = DatabaseController(view=self)
        
        self.editScreen = EditCabinetScreen(parent=self, controller=self.controller)
        
        button_font = ctk.CTkFont(size=38, weight="bold")
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=lambda: self.controller.show_frame("ChooseCabinetScreen")
        ).place(relx=.10, rely=.10, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Edit Info",
            command=lambda: self.controller.show_frame("EditCabinetScreen")
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.30, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Add Box",
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.50, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Manual Control",
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.70, anchor=ctk.CENTER)
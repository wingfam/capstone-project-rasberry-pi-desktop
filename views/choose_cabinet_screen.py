import customtkinter as ctk
from constants.image_imports import home_image

class ChooseCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.controller = controller
        button_font = ctk.CTkFont(size=38, weight="bold")
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=home_image,
            command=lambda: self.controller.show_frame("MainScreen"),
        ).place(relx=.90, rely=.10, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Cabinet 1",
            command=lambda: self.setCabinetId("1")
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.30, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Cabinet 2",
            command=lambda: self.setCabinetId("2")
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.50, anchor=ctk.CENTER)
    
    def setCabinetId(self, cabinetId):
        self.controller.cabinetId = cabinetId
        self.controller.show_frame("ConfigScreen")
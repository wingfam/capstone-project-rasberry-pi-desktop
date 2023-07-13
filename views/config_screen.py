import customtkinter as ctk
import tkinter as tk

class ConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.controller = controller
        button_font = ctk.CTkFont(size=38, weight="bold")
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Cabinet Info",
            command=lambda: self.controller.show_frame("CabinetInfo")
        ).place(relwidth=.45, relheight=.15, relx=.25, rely=.35, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="GPIO state"
        ).place(relwidth=.45, relheight=.15, relx=.75, rely=.35, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Test Control"
        ).place(relwidth=.45, relheight=.15, relx=.25, rely=.65, anchor=ctk.CENTER)
        
        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Modify Info"
        ).place(relwidth=.45, relheight=.15, relx=.75, rely=.65, anchor=ctk.CENTER)
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
            text="Control Box"
        ).place(relwidth=.35, relheight=.15, relx=.5, rely=.25, anchor=ctk.CENTER)
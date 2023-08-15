import customtkinter as ctk

from tkinter import ttk, CENTER
from constants.image_imports import back_image
from controllers.pre_config_controller import PreConfigController
from widgets.keypad import Keypad

class PreConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.root = root
        self.configController = PreConfigController(self)
        self.input_master_code = ctk.StringVar()
        
        text_font = ctk.CTkFont(size=38, weight="bold")
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=lambda: self.root.show_frame("MainScreen"),
        ).place(relx=.95, rely=.10, anchor=ctk.CENTER)
        
        self.master_code_label = ttk.Label(
            master=self,
            background="white",
            font=ctk.CTkFont(size=20),
            text="Nhập mã master code để vào config"
        )
                
        self.master_code_entry = ttk.Entry(
            master=self,
            justify="center",
            font=text_font,
            textvariable=self.input_master_code,
        )
        
        self.check_code_button = ctk.CTkButton(
            master=self,
            width=10,
            height=80,
            corner_radius=15.0,
            font=text_font,
            text="Confirm",
            command=self.verify
        ).place(relwidth=.4, relx=.28, rely=.71, anchor=ctk.CENTER)
        
        self.keypad = Keypad(self)
        self.keypad.target = self.master_code_entry
        self.keypad.place(relx=.78, rely=.5, anchor=CENTER)
        self.master_code_label.place(relx=.26, rely=.25, anchor=CENTER)
        self.master_code_entry.place(relwidth=.4, relheight=.15, relx=.28, rely=.4, anchor=CENTER)
    
    def verify(self):
        isConfirm = self.configController.check_master_code(self.input_master_code)
        if isConfirm:
            self.root.show_frame("ChooseCabinetScreen")
 
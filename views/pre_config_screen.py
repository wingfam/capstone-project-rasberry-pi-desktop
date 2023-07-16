import customtkinter as ctk
from tkinter import ttk, CENTER
from services.auth import firebase_login
from services.firebase_config import firebaseDB
from constants.image_imports import back_image
from widgets.keypad import Keypad

class PreConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.controller = controller
        self.configController = ConfigController(self)
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
            command=lambda: self.controller.show_frame("MainScreen"),
        ).place(relx=.95, rely=.10, anchor=ctk.CENTER)
        
        self.master_code_label = ttk.Label(
            master=self,
            background="white",
            font=ctk.CTkFont(size=20),
            text="Nhập mã master code để vào config"
        )
        self.master_code_label.place(relx=.26, rely=.25, anchor=CENTER)
        
        self.master_code_entry = ttk.Entry(
            master=self,
            justify="center",
            font=text_font,
            textvariable=self.input_master_code,
        )
        self.master_code_entry.place(relwidth=.4, relheight=.15, relx=.28, rely=.4, anchor=CENTER)
        
        self.check_code_button = ctk.CTkButton(
            master=self,
            width=10,
            height=80,
            corner_radius=15.0,
            font=text_font,
            text="Confirm",
            command=lambda: self.verify()
        ).place(relwidth=.4, relx=.28, rely=.71, anchor=ctk.CENTER)
        
        self.keypad = Keypad(self)
        self.keypad.target = self.master_code_entry
        self.keypad.place(relx=.78, rely=.5, anchor=CENTER)
    
    def verify(self):
        isConfirm = self.configController.check_master_code(self.input_master_code)
        if isConfirm:
            self.controller.show_frame("ConfigScreen")
    
class ConfigController():
    def __init__(self, view):
        self.view = view
    
    def check_master_code(self, input_data):
        isConfirm = False
        isError = False
        error_text= ""
        
        try:
            # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
            fb_login = firebase_login()
            input_code = input_data.get()
            
            fb_master_code = firebaseDB.child("MasterCode").order_by_child(
                "code").equal_to(input_code).get(fb_login["idToken"]).val()
            
            if fb_master_code != None and input_code == "111111":
                isError = True
                error_text = "Master code is incorrect!"
                return self.view.master_code_label.configure(
                    text=error_text,
                    foreground="red",
                )
            else:
                isConfirm = True
                
        except IndexError:
            isError = True
            error_text = "Use default code to enter"
            
            if input_code == "111111":
                print("Enter with default master code")
        
        if isError:
            return self.view.master_code_label.configure(
                text=error_text,
                foreground="red",
            )
        
        print("Master code is correct!")
        return isConfirm
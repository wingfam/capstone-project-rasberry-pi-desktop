import customtkinter as ctk
from tkinter import ttk, CENTER
from services.auth import firebase_login
from services.firebase_config import firebaseDB

class PreConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.parentController = controller
        self.configController = ConfigController(self)
        self.input_master_code = ctk.StringVar()
        
        text_font = ctk.CTkFont(size=38, weight="bold")
        
        self.master_code_label = ttk.Label(
            master=self,
            background="white",
            font=ctk.CTkFont(size=20),
            text="Nhập mã master code để vào config"
        )
        self.master_code_label.place(relx=.43, rely=.25, anchor=CENTER)
        
        self.master_code_entry = ttk.Entry(
            master=self,
            width=10,
            justify="center",
            font=text_font,
            textvariable=self.input_master_code,
        ).place(relwidth=0.5, relheight=0.15, relx=.5, rely=.4, anchor=CENTER)
        
        self.check_code_button = ctk.CTkButton(
            master=self,
            width=10,
            height=80,
            corner_radius=15.0,
            font=text_font,
            text="Confirm",
            command=lambda: self.verify()
        ).place(relwidth=0.5, relx=.5, rely=.60, anchor=ctk.CENTER)
    
    def verify(self):
        isConfirm = self.configController.check_master_code(self.input_master_code)
        if isConfirm:
            self.parentController.show_frame("ConfigScreen")
    
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
                self.view.master_code_label.place(relx=.38, rely=.25, anchor=CENTER)
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
            self.view.master_code_label.place(relx=.38, rely=.25, anchor=CENTER)
            return self.view.master_code_label.configure(
                text=error_text,
                foreground="red",
            )
        
        print("Master code is correct!")
        return isConfirm
import customtkinter as ctk
from tkinter import StringVar, ttk
from controllers.instruction_controller import confirm_task, update_firebase

class InstructionScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        self.root = root
        
        self.boxId = StringVar()
        self.task = StringVar()
        
        ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=24),
            bg_color="white",
            text_color="black",
            text="Tủ của bạn là số: "
        ).place(x=445, y=118)
        
        ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=24),
            bg_color="white",
            text_color="black",
            text="Hãy nhấn nút xác nhận để mở khóa tủ. \nSau khi bỏ hàng vào, vui lòng đóng kín cửa tủ lại."
        ).place(x=445, y=205)
        
        self.nameBox_label = ttk.Label(
            master=self,
            font=ctk.CTkFont(size=24),
            background="white",
            foreground="red",
            text=""
        )
        self.nameBox_label.place(x=635.0, y=114.5)
        
        self.button_confirm = ctk.CTkButton(
            master=self,
            width=503,
            height=86,
            bg_color="#FFFFFF",
            border_width=1,
            text="Xác Nhận",
            text_color="white",
            font=ctk.CTkFont(size=24),
            command=self.check_package,
        )
        self.button_confirm.place(x=445.0, y=375.0)
        
        self.error_label = ttk.Label(
            self, 
            background="white", 
            font=ctk.CTkFont(size=16),
            text="", 
        )
        self.error_label.place(
            x=445.0,
            y=485.0,
        )
        
    def check_package(self):
        isConfirm = False
        task = self.task.get()
        
        boxId = self.boxId.get()
        globalBoxData = self.root.globalBoxData
        
        for key, value in globalBoxData.items():
            if boxId == value['id']:
                isConfirm = confirm_task(value, task)
                break
                
        if isConfirm:
            update_firebase(self, task)
            self.root.show_frame("CompletionScreen")
        else:
            self.root.show_frame("MainScreen")
        
        self.root.app_data.clear()
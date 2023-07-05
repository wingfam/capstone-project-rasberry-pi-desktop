import customtkinter as ctk
from tkinter import StringVar, ttk, Canvas
from controllers.instruction import confirm_task

class InstructionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        self.controller = controller
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
            text="Sau khi để hàng vào tủ, vui lòng đóng kín cửa tủ lại. \nSau đó nhấn nút Xác Nhận để hoàn tất thao tác."
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
            command=lambda: self.check_package(),
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
        task = self.task.get()
        isComplete = confirm_task(self, task=task)
        if isComplete:
            self.controller.show_frame("CompletionScreen")

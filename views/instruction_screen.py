import customtkinter as ctk
from tkinter import ttk, Canvas
from controllers.instruction import confirm_task

class InstructionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 600,
            width = 1024,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        canvas.create_text(
            445.0,
            118.0,
            anchor="nw",
            text="Tủ của bạn là số: ",
            fill="#333333",
            font=("Roboto", 24 * -1)
        )
        
        self.locker_name_label = ttk.Label(
            master=self,
            font=ctk.CTkFont(size=24),
            background="white",
            foreground="red",
            text=""
        )
        self.locker_name_label.place(x=635.0, y=114.5)
        
        canvas.create_text(
            445.0,
            118.0,
            anchor="nw",
            text="Tủ của bạn là số: ",
            fill="#333333",
            font=("Roboto", 24 * -1)
        )
        
        canvas.create_text(
            445.0,
            205.0,
            anchor="nw",
            text="Sau khi để hàng vào tủ, vui lòng đóng kín cửa tủ lại. \nSau đó nhấn nút Xác Nhận để hoàn tất thao tác.",
            fill="#333333",
            font=("Roboto", 24 * -1)
        )
        
        canvas.create_rectangle(
            55.0,
            122.0,
            363.0,
            462.0,
            fill="#FFFFFF",
            outline="black")
        
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
        self.button_confirm.place(
            x=445.0,
            y=375.0,
        )
        
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
        task = "delivery"
        data = {
            "BookingCodeId": self.controller.app_data["BookingCodeId"],
            "Status": self.controller.app_data["Status"],
        }
        isComplete = confirm_task(self, data=data, task=task)
        if isComplete:
            self.controller.show_frame("CompletionScreen")

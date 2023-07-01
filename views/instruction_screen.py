import customtkinter as ctk
from tkinter import ttk, Canvas

class InstructionScreen(ctk.CTkToplevel):
    # Class attribute that indicates whether this child window
    # is being used (alive) or not.
    alive = False
    
    def __init__(self, info):
        ctk.CTkToplevel.__init__(self, info)
        self.geometry("1024x600")
        # self.attributes('-fullscreen', True)
        self.title("Smart Locker")
        self.attributes("-topmost", True)
        self.focus()
        self.grab_set()
        # Set the window as alive once created.
        self.__class__.alive = True
        
        self.info = info
        
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
            text="Hướng dẫn:",
            fill="#333333",
            font=("RobotoRoman Bold", 24 * -1)
        )
        
        canvas.create_text(
            445.0,
            166.0,
            anchor="nw",
            text="Tủ của bạn là số: ",
            fill="#333333",
            font=("Roboto", 24 * -1)
        )
        
        locker_name_label = ttk.Label(
            self,
            font=ctk.CTkFont(size=24),
            text=self.info["LockerName"], 
        )
        self.locker_name_label.grid(
            padx=642,
            pady=166,
        )
        locker_name_label.cget()
        
        canvas.create_text(
            445.0,
            205.0,
            anchor="nw",
            text="Sau khi mở tủ, vui lòng đóng kín cửa tủ lại. \nSau 30 giây nếu tủ chưa được mở, cửa tủ sẽ \ntự động khóa. Bạn cần nhập lại mã để mở tủ.",
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
            command= print(locker_name_label.cget()),
        )
        self.button_confirm.place(
            x=445.0,
            y=375.0,
        )

    def destroy(self):
        # Restore the attribute on close.
        self.__class__.alive = False
        return super().destroy()
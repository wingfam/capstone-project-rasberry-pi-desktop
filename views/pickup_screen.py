import customtkinter as ctk
from tkinter import ttk, Canvas, Image
from PIL import Image
from widgets.keypad import Keypad

class PickupScreen(ctk.CTkToplevel):
    # Class attribute that indicates whether this child window
    # is being used (alive) or not.
    alive = False
    
    def __init__(self, *args, **kwargs):
        ctk.CTkToplevel.__init__(self, *args, **kwargs)
        self.geometry("1024x600")
        # self.attributes('-fullscreen', True)
        self.title("Smart Locker")
        self.attributes("-topmost", True)
        self.focus()
        self.grab_set()
        # Set the window as alive once created.
        self.__class__.alive = True
        
        back_image = ctk.CTkImage(light_image=Image.open("assets/images/button_back.png"), size=[44, 44])
        
        canvas = Canvas(
            master=self,
            bg = "#FFFFFF",
            height = 600,
            width = 1024,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        canvas.create_text(
            48.0,
            280.0,
            anchor="nw",
            text="Lưu ý: mã có thời hạn là 10 phút. Nếu mã hết hạn, \nhãy yêu cầu người nhận hàng gửi lại mã khác.",
            fill="#535353",
            font=("Roboto", 20 * -1)
        )
        
        canvas.create_text(
            568.0,
            108.0,
            anchor="nw",
            text="Nhập mã unlock tủ",
            fill="#535353",
            font=("Roboto", 20 * -1)
        )
        
        canvas.create_rectangle(
            567.0,
            166.0,
            897.0,
            496.0,
            fill="#DDDDDD",
            outline="black")
        
        entry_code = ctk.CTkEntry(
            master=self,
            fg_color="#FFFFFF",
            width=467.0,
            height=82.0,
            text_color="black",
            font=ctk.CTkFont(size=48),
        )
        entry_code.place(
            x=42.0,
            y=166.0,
        )
        
        self.button_confirm = ctk.CTkButton(
            master=self,
            width=442,
            height=64,
            bg_color="#FFFFFF",
            border_width=1,
            text="Xác Nhận",
            text_color="white",
            font=ctk.CTkFont(size=24),
            command=lambda: print("Validate unlock code"),
        )
        self.button_confirm.place(
            x=48.0,
            y=432.0,
        )
        
        self.button_back = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=lambda: self.destroy(),
        )
        self.button_back.place(
            x=951.0,
            y=38.0,
        )
        
        self.keypad = Keypad(self)
        self.keypad.target = entry_code
        self.keypad.place(
            x=567,
            y=156,
        )
    
    def destroy(self):
        # Restore the attribute on close.
        self.__class__.alive = False
        return super().destroy()
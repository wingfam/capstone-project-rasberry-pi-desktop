import customtkinter as ctk
from tkinter import StringVar, ttk, Canvas, Image
from PIL import Image
from widgets.keypad import Keypad
from controllers.delivery import check_booking_code, get_booked_locker

back_image = ctk.CTkImage(light_image=Image.open("assets/images/button_back.png"), size=[44, 44])
        
class DeliveryScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        self.parent = parent
        self.controller = controller
        
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
            text="Nhập mã booking",
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
        
        self.entry_code = ctk.CTkEntry(
            master=self,
            fg_color="#FFFFFF",
            width=467.0,
            height=82.0,
            text_color="black",
            font=ctk.CTkFont(size=48),
        )
        self.entry_code.place(
            x=42.0,
            y=166.0,
        )
        
        self.label = ttk.Label(
            self, 
            background="white", 
            font=ctk.CTkFont(size=16),
            text="", 
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
            command=lambda: self.validate(),
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
            command=lambda: self.restart(),
        )
        self.button_back.place(
            x=951.0,
            y=528.0,
        )
        
        self.keypad = Keypad(self)
        self.keypad.target = self.entry_code
        self.keypad.place(
            x=567,
            y=156,
        )
        
    
    def validate(self):
        item_list = check_booking_code(self=self, input_data=self.entry_code)
        if item_list:
            get_booked_locker(self, fb_login=item_list[0], fb_item_list=item_list[1])
            locker_name = self.controller.app_data["LockerName"]
            self.controller.frames["InstructionScreen"].locker_name_label.configure(text=locker_name)
            self.controller.show_frame("InstructionScreen")
        else:
            pass
    
    def restart(self):
        self.refresh()
        self.event_delete("<<DeliveryScreen>>")
        self.controller.show_frame("MainScreen")
        
    def refresh(self):
        self.entry_code.delete(0, "end")
        self.label.grid_remove()

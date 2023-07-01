import customtkinter as ctk
from tkinter import ttk, Canvas, Image
from PIL import Image
from controllers.delivery_controller import check_booking_code, get_booking_info
from views.instruction_screen import InstructionScreen
from widgets.keypad import Keypad

# TODO: Chyển tất cả frame sang window
class DeliveryScreen(ctk.CTkToplevel):
    # Class attribute that indicates whether this child window
    # is being used (alive) or not.
    alive = False

    def __init__(self, *args, **kwargs):
        ctk.CTkToplevel.__init__(self,  *args, **kwargs)
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
            command=lambda: self.validate(self.entry_code),
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
        self.keypad.target = self.entry_code
        self.keypad.place(
            x=567,
            y=156,
        )
    
    def validate(self, entry_code):
        item_list = check_booking_code(self=self, input_data=entry_code)
        if item_list:
            booking_info = get_booking_info(fb_login=item_list[0], fb_item_list=item_list[1])
            self.open_instruction_screen(info=booking_info)
            self.destroy()
        else:
            pass
    
    def open_instruction_screen(self, info):
        print("ERROR?")
        #TODO: Fix AttributeError: 'dict' object has no attribute 'tk'
        if not InstructionScreen.alive:
            self.secondary_window = InstructionScreen(info=info)
    
    def destroy(self):
        # Restore the attribute on close.
        self.__class__.alive = False
        return super().destroy()

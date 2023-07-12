import customtkinter as ctk
from tkinter import ttk
from widgets.keypad import Keypad
from constants.image_constants import back_image
from controllers.delivery_controller import check_booking_code, update_app_data
        
class DeliveryScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        self.parent = parent
        self.controller = controller
        self.back_image = back_image
        
        ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            text="Nhập mã booking"
        ).place(x=568, y=108)
        
        ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            text="Lưu ý: mã có thời hạn là 10 phút. Nếu mã hết hạn,\nhãy yêu cầu người nhận hàng gửi lại mã khác."
        ).place(x=48, y=280)
        
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
        
        self.label_error = ttk.Label(
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
        self.button_confirm.place(x=48.0,y=432.0)
        
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
        self.button_back.place(x=951.0,y=528.0)
        
        self.keypad = Keypad(self)
        self.keypad.target = self.entry_code
        self.keypad.place(x=567,y=156)
        
    
    def validate(self):
        item_list = check_booking_code(self, input_data=self.entry_code)
        if item_list:
            update_app_data(self, fb_login=item_list[0], fb_item_list=item_list[1])
            nameBox = self.controller.app_data["nameBox"]
            self.controller.frames["InstructionScreen"].nameBox_label.configure(text=nameBox)
            self.controller.frames["InstructionScreen"].task.set("delivery")
            self.controller.show_frame("InstructionScreen")
    
    def set_controller(self, controller):
        self.deliveryController = controller
    
    def set_model(self, model):
        self.boxModel = model
    
    def restart(self):
        self.refresh()
        self.controller.show_frame("MainScreen")
        
    def refresh(self):
        self.entry_code.delete(0, "end")
        self.label_error.grid_remove()

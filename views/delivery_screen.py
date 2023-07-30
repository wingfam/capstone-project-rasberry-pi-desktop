import customtkinter as ctk

from tkinter import ttk
from widgets.keypad import Keypad
from constants.image_imports import back_image
from controllers.delivery_controller import DeliveryController
        
class DeliveryScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        self.parent = parent
        self.root = root
        self.back_image = back_image
        self.deliveryController = DeliveryController(self)
        
        self.notice_label1 = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            text="Nhập mã booking"
        )
        
        self.notice_label2 = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            text="Lưu ý: mã có thời hạn là 10 phút. Nếu mã hết hạn,\nhãy yêu cầu người nhận hàng gửi lại mã khác."
        )
        
        self.entry_code = ttk.Entry(
            master=self,
            justify="center",
            font=ctk.CTkFont(size=48),
        )
        
        self.label_error = ttk.Label(
            master=self, 
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
            command=self.go_to_instruction_screen,
        )
        
        self.button_back = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=self.go_to_main_screen,
        )
        
        
        self.keypad = Keypad(self)
        self.keypad.target = self.entry_code
        self.keypad.place(x=567,y=156)
        
        self.notice_label1.place(x=568, y=108)
        self.notice_label2.place(x=48, y=280)
        self.button_confirm.place(relx=.45, rely=.70, anchor=ctk.CENTER)
        self.button_back.place(relx=.95, rely=.10, anchor=ctk.CENTER)
        self.entry_code.place(relwidth=.4, relheight=.15, relx=.28, rely=.32, anchor=ctk.CENTER)
        
    
    def validate(self):
        item_list = self.deliveryController.check_booking_code(input_data=self.entry_code)
        if item_list:
            self.deliveryController.update_app_data(fb_login=item_list[0], fb_item_list=item_list[1])
            
            nameBox = self.root.app_data["nameBox"]
            boxId = self.root.app_data["boxId"]
            
            self.root.frames["InstructionScreen"].nameBox_label.configure(text=nameBox)
            self.root.frames["InstructionScreen"].boxId.set(boxId)
            self.root.frames["InstructionScreen"].task.set("delivery")
            
            self.go_to_instruction_screen()
    
    def refresh(self):
        self.entry_code.delete(0, "end")
        self.label_error.grid_remove()
        
    def go_to_main_screen(self):
        self.refresh()
        self.root.show_frame("MainScreen")
        
    def go_to_instruction_screen(self):
        self.refresh()
        self.root.show_frame("InstructionScreen")

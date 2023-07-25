import customtkinter as ctk
from widgets.keypad import Keypad
from constants.image_imports import back_image
from controllers.pickup_controller import PickupController

class PickupScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        self.parent = parent
        self.root = root
        self.back_image = back_image
        self.pickupController = PickupController(self)
        
        ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            text="Lưu ý: nếu mã hết hạn, hãy yêu liên lạc với admin \nđể nhận mã khác."
        ).place(x=48, y=288)
        
        ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            text="Nhập mã unlock tủ"
        ).place(x=568, y=108)
        
        self.entry_code = ctk.CTkEntry(
            master=self,
            fg_color="#FFFFFF",
            width=467.0,
            height=82.0,
            text_color="black",
            font=ctk.CTkFont(size=48),
        )
        self.entry_code.place(x=42.0,y=166.0)
        
        self.label_error = ctk.CTkLabel(
            self, 
            bg_color="white", 
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
            command=self.validate,
        )
        self.button_confirm.place(x=48.0,y=432.0)
        
        self.button_back = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=self.back_image,
            command=self.go_to_main_screen,
        )
        self.button_back.place(x=951.0,y=528.0)
        
        self.keypad = Keypad(self)
        self.keypad.target = self.entry_code
        self.keypad.place(x=567,y=156)
    
    def validate(self):
        item_list = self.pickupController.check_unlock_code(input_data=self.entry_code)
        if item_list:
            self.pickupController.update_app_data(fb_login=item_list[0], fb_item_list=item_list[1])
            nameBox = self.root.app_data["nameBox"]
            self.root.frames["InstructionScreen"].nameBox_label.configure(text=nameBox)
            self.root.frames["InstructionScreen"].task.set("pickup")
            self.root.show_frame("InstructionScreen")
    
    def restart(self):
        self.refresh()
        self.root.show_frame("MainScreen")
        
    def refresh(self):
        self.entry_code.delete(0, "end")
        self.label_error.grid_remove()
        
    def go_to_main_screen(self):
        self.refresh()
        self.root.show_frame("MainScreen")
import customtkinter as ctk

from tkinter import ttk
from controllers.config_controller import DatabaseController
from widgets.keypad import Keypad
from constants.image_imports import back_image
from constants.string_constants import pickup_notice_label
from controllers.pickup_controller import PickupController
from widgets.loading_window import LoadingWindow

class PickupScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.parent = parent
        self.root = root
        self.back_image = back_image
        
        self.databaseController = DatabaseController(self)
        self.pickupController = PickupController(self)
        
        self.inputUnlockCode = ctk.StringVar()
        
        self.inputUnlockCode.trace("w", self.limitSizeCode)
        
        self.notice_label1 = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            text="Nhập mã unlock tủ"
        )
        
        self.notice_label2 = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color="white",
            text_color="black",
            justify='left',
            text=pickup_notice_label
        )
        
        self.entry_code = ttk.Entry(
            master=self,
            justify="center",
            font=ctk.CTkFont(size=48),
            textvariable=self.inputUnlockCode,
        )
        
        self.label_error = ttk.Label(
            master=self, 
            background="white", 
            font=ctk.CTkFont(size=16),
            text="", 
        )
        
        self.button_confirm = ctk.CTkButton(
            master=self,
            width=430,
            height=64,
            bg_color="#FFFFFF",
            border_width=1,
            text="Xác Nhận",
            text_color="white",
            font=ctk.CTkFont(size=34),
            command=self.do_validate,
        )
        
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
        
        self.keypad = Keypad(self)
        self.keypad.target = self.entry_code
        
        self.keypad.place(relx=.75, rely=.55, anchor=ctk.CENTER)
        self.notice_label1.place(relx=.65, rely=.20, anchor=ctk.CENTER)
        self.notice_label2.place(relx=.28, rely=.45, anchor=ctk.CENTER)
        self.label_error.grid(padx=95, pady=110)
        self.button_confirm.place(relx=.28, rely=.75, anchor=ctk.CENTER)
        self.button_back.place(relx=.10, rely=.10, anchor=ctk.CENTER)
        self.entry_code.place(relwidth=.4, relheight=.10, relx=.28, rely=.32, anchor=ctk.CENTER)
    
    def do_validate(self):
        self.loadingWindow = LoadingWindow(self, self.root)
        self.loadingWindow.after(500, self.validate)
        
    def validate(self):
        try:
            unlockCode = self.inputUnlockCode.get()
            self.button_confirm.configure(state="disabled")
            bookingId = self.pickupController.check_unlock_code(unlockCode)
            
            if bookingId:
                self.pickupController.update_app_data(bookingId)
                
                nameBox = self.root.app_data["nameBox"]
                boxId = self.root.app_data["boxId"]
                
                self.root.frames["InstructionScreen"].nameBox_label.configure(text=nameBox)
                self.root.frames["InstructionScreen"].boxId.set(boxId)
                self.root.frames["InstructionScreen"].task.set("pickup")
                
                self.go_to_instruction_screen()
        except Exception as e:
            print(e)
        finally:
            self.loadingWindow.destroy()  
            self.button_confirm.after(1500, self.enable_confirm_button)
    
    def limitSizeCode(self, *args):
        # limit the size of master code entry
        value = self.inputUnlockCode.get()
        if len(value) > 6: self.inputUnlockCode.set(value[:6])
        
    def refresh(self):
        self.entry_code.delete(0, "end")
        self.label_error.configure(text="", foreground="red")
        
    def go_to_main_screen(self):
        self.refresh()
        self.root.show_frame("MainScreen")
        
    def go_to_instruction_screen(self):
        self.refresh()
        self.root.show_frame("InstructionScreen")
        
    def enable_confirm_button(self):
        self.button_confirm.configure(state="normal")
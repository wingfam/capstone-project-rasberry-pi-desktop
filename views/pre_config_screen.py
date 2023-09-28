import customtkinter as ctk

from tkinter import ttk, CENTER
from constants.image_imports import back_image, show_pass_image, hide_pass_image
from controllers.config_controller import DatabaseController
from widgets.keypad import Keypad
from widgets.loading_window import LoadingWindow

class PreConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.root = root
        
        self.databaseController = DatabaseController(self)
        
        self.inputMasterCode = ctk.StringVar()
        self.isShowCode = ctk.BooleanVar()
        
        # Add limitSizeCode callback to input_master_code
        self.inputMasterCode.trace("w", self.limitSizeCode)
        
        text_font = ctk.CTkFont(size=38, weight="bold")
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=self.go_to_main_screen,
        ).place(relx=.10, rely=.10, anchor=ctk.CENTER)
        
        self.error_label = ttk.Label(
            master=self,
            background="white",
            font=ctk.CTkFont(size=20),
            text=""
        )
        
        self.master_code_label = ttk.Label(
            master=self,
            background="white",
            font=ctk.CTkFont(size=20),
            text="Nhập mã master code để vào config"
        )
                
        self.master_code_entry = ttk.Entry(
            master=self,
            justify="center",
            font=text_font,
            show="*",
            textvariable=self.inputMasterCode,
        )
        
        self.check_code_button = ctk.CTkButton(
            master=self,
            width=10,
            height=80,
            corner_radius=15.0,
            font=text_font,
            text="Xác Nhận",
            command=self.do_check_master_code
        )
        
        self.show_hide_code_btn = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=hide_pass_image,
            command=self.show_hide_master_code,
        )
        
        self.keypad = Keypad(self)
        self.keypad.target = self.master_code_entry
        
        self.keypad.place(relx=.78, rely=.5, anchor=CENTER)
        self.error_label.place(relx=.26, rely=.15, anchor=CENTER)
        self.master_code_label.place(relx=.26, rely=.45, anchor=CENTER)
        self.master_code_entry.place(relwidth=.4, relheight=.15, relx=.28, rely=.30, anchor=CENTER)
        self.check_code_button.place(relwidth=.4, relx=.28, rely=.71, anchor=ctk.CENTER)
        self.show_hide_code_btn.place(relx=.45, rely=.30, anchor=ctk.CENTER)
    
    def do_check_master_code(self):
        self.loadingWindow = LoadingWindow(self, self.root)
        self.loadingWindow.after(500, self.check_master_code)
        
    def check_master_code(self):
        inputCode = self.inputMasterCode.get()
        foundMasterCode = self.databaseController.get_masterCode(inputCode)
        
        try:
            if not foundMasterCode:
                error_text = "Mã master không đúng"
                return self.error_label.configure(text=error_text, foreground="red")
                
            for value in foundMasterCode.values():
                masterCodeStatus =  int(value['masterCodeStatus'])
                if masterCodeStatus == 1:
                    self.go_to_config_screen()
                else:
                    error_text = "Mã master không thể dùng vào lúc này"
                    return self.error_label.configure(text=error_text, foreground="red")
        except Exception as e:
            print("Check master code error: " + e)
        finally:
            self.loadingWindow.destroy()
    
    def show_hide_master_code(self):
        if not self.isShowCode.get():
            self.isShowCode.set(True)
            self.master_code_entry.configure(show="")
            self.show_hide_code_btn.configure(require_redraw=True, image=show_pass_image)
        else:
            self.isShowCode.set(False)
            self.master_code_entry.configure(show="*")
            self.show_hide_code_btn.configure(require_redraw=True, image=hide_pass_image)
    
    def limitSizeCode(self, *args):
        # limit the size of master code entry
        value = self.inputMasterCode.get()
        if len(value) > 6: self.inputMasterCode.set(value[:6])
    
    def refresh(self):
        self.inputMasterCode.set("")
        self.error_label.configure(text="")
        self.master_code_entry.configure(show="*")
        self.show_hide_code_btn.configure(require_redraw=True, image=hide_pass_image)
        
    def go_to_main_screen(self):
        self.refresh()
        self.root.show_frame("MainScreen")
        
    def go_to_config_screen(self):
        self.refresh()
        self.root.show_frame("ConfigScreen")
import customtkinter as ctk

from tkinter import StringVar, ttk
from constants.string_constants import instruction_label
from controllers.instruction_controller import InstructionController

class InstructionScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.root = root
        
        self.instructionController = InstructionController(view=self)
        
        self.instruction_label  = instruction_label
        self.boxId = StringVar()
        self.task = StringVar()
        
        self.notice_label1 = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=24),
            bg_color="white",
            text_color="black",
            text="Tủ của bạn là số: "
        )
        
        self.notice_label2 = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=24),
            bg_color="white",
            text_color="black",
            justify='left',
            anchor='e',
            text=self.instruction_label,
        )
        
        self.nameBox_label = ttk.Label(
            master=self,
            font=ctk.CTkFont(size=24),
            background="white",
            foreground="red",
            text=""
        )
        
        
        self.button_confirm = ctk.CTkButton(
            master=self,
            bg_color="#FFFFFF",
            border_width=1,
            text="Xác Nhận",
            text_color="white",
            font=ctk.CTkFont(size=34),
            command=self.check_package,
        )
        
        
        self.notice_label1.place(relx=.45, rely=.18)
        self.notice_label2.place(relx=.45, rely=.25)
        self.nameBox_label.place(relx=.64, rely=.1755)
        self.button_confirm.place(relwidth=.4, relheight=.15, relx=.45, rely=.55)
        
        
    def check_package(self):
        isConfirm = False
        task = self.task.get()
        
        boxId = self.boxId.get()
        globalBoxData = self.root.globalBoxData
        
        for key, value in globalBoxData.items():
            if boxId == value['id']:
                isConfirm = self.instructionController.confirm_task(value, task)
                break
                
        if isConfirm:
            self.instructionController.update_firebase(task)
            self.root.show_frame("CompletionScreen")
        else:
            self.root.show_frame("MainScreen")
        
        self.root.app_data.clear()
import customtkinter as ctk
from constants.image_imports import home_image, add_image, refresh_image
from controllers.config_controller import ChooseCabinetController

class ChooseCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.controller = controller
        self.cabinetController = ChooseCabinetController(view=self)
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=home_image,
            command=lambda: self.controller.show_frame("MainScreen"),
        ).place(relx=.10, rely=.10, anchor=ctk.CENTER)
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=add_image,
            command=lambda: self.controller.show_frame("AddCabinetScreen"),
        ).place(relx=.90, rely=.10, anchor=ctk.CENTER)
        
        
        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=refresh_image,
            command=lambda: self.reload(),
        ).place(relx=.90, rely=.20, anchor=ctk.CENTER)
        
        self.cabinetButtonFrame = CabinetButtonFrame(self)
        self.cabinetButtonFrame.place(relwidth=.5, relheight=.95, rely=.5, relx=.5, anchor=ctk.CENTER)
    '''TODO: find a way to redraw frame'''
    def reload(self):
        self.cabinetButtonFrame.after(500, self.cabinetButtonFrame.__init__(self))
    
    def print(self):
        print("Page reloaded")

class CabinetButtonFrame(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.parent = parent
        
        cabinets = self.parent.cabinetController.get_all_cabinet()
        self.placeCabinetButton(cabinetList=cabinets)
        
    def placeCabinetButton(self, cabinetList):
        count = 0;
        for key, value in cabinetList.items():
            count += 1
            buttonText = "Cabinet " + str(count)
            ctk.CTkButton(
                master=self,
                anchor=ctk.CENTER,
                font=ctk.CTkFont(size=38, weight="bold"),
                text=buttonText,
                command=lambda: self.setCabinetId(key, value)
            ).pack(pady=10, ipadx=20, ipady=10)
    
    def setCabinetId(self, cabinetId, cabinetValues):
        self.parent.controller.cabinetId = cabinetId
        self.parent.controller.cabinetValues = cabinetValues
        self.parent.controller.show_frame("ConfigScreen")
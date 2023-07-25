import customtkinter as ctk
from tkinter import CENTER
from constants.image_imports import completion_image

class CompletionScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        self.root = root
        self.completion_image = completion_image
        
        self.label_completion = ctk.CTkLabel(master=self, anchor="center", image=completion_image, text="")
        self.label_completion.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    def go_back(self):
        self.event_delete("<<GoBackMainScreen>>")
        self.root.frames["DeliveryScreen"].restart()
        self.root.frames["PickupScreen"].restart()
        self.root.show_frame("MainScreen")
    
    def on_show_frame(self):
        self.root.app_data.clear()
        self.after(3000, self.go_back)

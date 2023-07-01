import customtkinter as ctk
from tkinter import Canvas, Image
from PIL import Image, ImageTk

class CompletionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        completion_image = ImageTk.PhotoImage(Image.open("assets/images/image_completion.png"), size=[64, 64])
        
        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 600,
            width = 1024,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        self.label = completion_image
        
        canvas.create_image(
            512.0,
            300.0,
            image=completion_image,
        )
   
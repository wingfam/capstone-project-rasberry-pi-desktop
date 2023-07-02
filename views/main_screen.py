import time
import customtkinter as ctk
from tkinter import ttk, Canvas, Image
from PIL import Image

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent
        
        self.delivery_image = ctk.CTkImage(light_image=Image.open("assets/images/image_2.png"), size=[233, 233])
        self.pickup_image = ctk.CTkImage(light_image=Image.open("assets/images/image_1.png"), size=[233, 233])
        
        canvas = Canvas(
            master=self,
            bg = "#FFFFFF",
            height = 600,
            width = 1024,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.pack(fill='both', expand=True)
        
        button_pickup = ctk.CTkButton(
            master=self,
            width=420,
            height=300,
            corner_radius=30,
            bg_color="white",
            image=self.pickup_image,
            compound="top",
            text="Lấy Hàng",
            font=ctk.CTkFont(size=48),
            command=lambda: controller.show_frame("PickupScreen"),
        )
        button_pickup.place(
            x=61.0,
            y=150.0,
        )
        
        button_delivery = ctk.CTkButton(
            master=self,
            width=420,
            height=300,
            corner_radius=30,
            bg_color="white",
            image=self.delivery_image,
            compound="top",
            text="Gửi Hàng",
            font=ctk.CTkFont(size=48),
            command=lambda: controller.show_frame("DeliveryScreen"),
        )
        button_delivery.place(
            x=542.5924682617188,
            y=150.0,
        )
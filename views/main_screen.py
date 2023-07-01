import customtkinter as ctk
from tkinter import Canvas, Image
from PIL import Image
from views.delivery_screen import DeliveryScreen
from views.pickup_screen import PickupScreen

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)
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
        canvas.place(x = 0, y = 0)
        
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
            command=lambda: print("Go to Pickup Screen"),
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
            command=lambda: self.open_delivery_screen(),
        )
        button_delivery.place(
            x=542.0,
            y=150.0,
        )

    def open_delivery_screen(self):
        if not DeliveryScreen.alive:
            self.secondary_window = DeliveryScreen()
    
    def open_pickup_screen(self):
        if not PickupScreen.alive:
            self.secondary_window = PickupScreen()

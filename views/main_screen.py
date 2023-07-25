import customtkinter as ctk
from constants.image_imports import delivery_image, pickup_image, config_image

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")
        
        self.delivery_image = delivery_image
        self.pickup_image = pickup_image
        self.config_image = config_image
        
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
            command=lambda: root.show_frame("PickupScreen"),
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
            command=lambda: root.show_frame("DeliveryScreen"),
        )
        button_delivery.place(
            x=542.5924682617188,
            y=150.0,
        )
        
        button_config = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=self.config_image,
            command=lambda: root.show_frame("ControlPinScreen"),
        )
        button_config.place(x=951.0,y=38.0)
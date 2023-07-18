import customtkinter as ctk
from PIL import Image

delivery_image = ctk.CTkImage(light_image=Image.open("assets/images/image_2.png"), size=[233, 233])
pickup_image = ctk.CTkImage(light_image=Image.open("assets/images/image_1.png"), size=[233, 233])
back_image = ctk.CTkImage(light_image=Image.open("assets/images/button_back.png"), size=[44, 44])
home_image = ctk.CTkImage(light_image=Image.open("assets/images/button_home.png"), size=[44, 44])
completion_image = ctk.CTkImage(light_image=Image.open("assets/images/image_completion.png"), size=[234, 200])
config_image = ctk.CTkImage(light_image=Image.open("assets/images/button_config.png"), size=[44, 44])
add_image = ctk.CTkImage(light_image=Image.open("assets/images/button_add.png"), size=[44, 44])

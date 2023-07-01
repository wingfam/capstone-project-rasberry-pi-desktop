import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, Canvas, Image
from PIL import Image, ImageTk
from views.main_screen import MainScreen
from views.delivery_screen import DeliveryScreen
from views.pickup_screen import PickupScreen
from controllers.delivery import check_booking_code, get_booked_locker
from widgets.keypad import Keypad

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("1024x600")
        self.title("Smart Locker")
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (MainScreen, DeliveryScreen, PickupScreen, InstructionScreen, CompletionScreen):
            frame = F(container, self)
            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(MainScreen)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class InstructionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        home_image = ctk.CTkImage(light_image=Image.open("assets/images/button_home.png"), size=[44, 44])
        back_image = ctk.CTkImage(light_image=Image.open("assets/images/button_back.png"), size=[44, 44])
        
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
        
        canvas.create_text(
            445.0,
            118.0,
            anchor="nw",
            text="Hướng dẫn:",
            fill="#333333",
            font=("RobotoRoman Bold", 24 * -1)
        )
        
        canvas.create_text(
            445.0,
            166.0,
            anchor="nw",
            text="Tủ của bạn là số: ",
            fill="#333333",
            font=("Roboto", 24 * -1)
        )
        
        nameCanvas = canvas.create_text(
            642.0,
            166.0,
            anchor="nw",
            text="02",
            fill="#000000",
            font=("Roboto", 24 * -1)
        )
        lockerName = canvas.itemcget(nameCanvas, 'text')
        
        
        canvas.create_text(
            445.0,
            205.0,
            anchor="nw",
            text="Sau khi mở tủ, vui lòng đóng kín cửa tủ lại. \nSau 30 giây nếu tủ chưa được mở, cửa tủ sẽ \ntự động khóa. Bạn cần nhập lại mã để mở tủ.",
            fill="#333333",
            font=("Roboto", 24 * -1)
        )
        
        canvas.create_rectangle(
            55.0,
            122.0,
            363.0,
            462.0,
            fill="#FFFFFF",
            outline="black")
        
        self.button_confirm = ctk.CTkButton(
            master=self,
            width=503,
            height=86,
            bg_color="#FFFFFF",
            border_width=1,
            text="Xác Nhận",
            text_color="white",
            font=ctk.CTkFont(size=24),
            command=lambda: controller.show_frame(CompletionScreen),
        )
        self.button_confirm.place(
            x=445.0,
            y=375.0,
        )
        
        self.button_home = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=home_image,
            command=lambda: controller.show_frame(MainScreen),
        )
        self.button_home.place(
            x=951.0,
            y=36.0,
        )
        
        self.button_back = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=lambda: controller.show_frame(DeliveryScreen),
        )
        self.button_back.place(
            x=951.0,
            y=528.0,
        )

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
        

if __name__ == "__main__":
    root = MainApp()
    root.mainloop()
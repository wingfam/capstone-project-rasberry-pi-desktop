import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, Canvas, Image
from PIL import Image, ImageTk
from controllers.delivery import verify_booking_code
# from controllers.delivery import verify_booking_code
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
        frame.event_generate("<<ShowMainScreen>>")
        frame.event_generate("<<ShowDeliveryScreen>>")
        frame.tkraise()

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.bind("<<ShowMainScreen>>", self.on_show_frame(event="<<ShowMainScreen>>"))
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
            command=lambda: controller.show_frame(PickupScreen),
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
            command=lambda: controller.show_frame(DeliveryScreen),
        )
        button_delivery.place(
            x=542.5924682617188,
            y=150.0,
        )
    
    def on_show_frame(self, event):
        if event:
            print("MainScreen is being shown...")

class DeliveryScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.bind("<<ShowDeliveryScreen>>", self.on_show_frame(event="<<ShowDeliveryScreen>>"))
        
        back_image = ctk.CTkImage(light_image=Image.open("assets/images/button_back.png"), size=[44, 44])
        
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
        
        canvas.create_text(
            48.0,
            280.0,
            anchor="nw",
            text="Lưu ý: mã có thời hạn là 10 phút. Nếu mã hết hạn, \nhãy yêu cầu người nhận hàng gửi lại mã khác.",
            fill="#535353",
            font=("Roboto", 20 * -1)
        )
        
        canvas.create_text(
            568.0,
            108.0,
            anchor="nw",
            text="Nhập mã booking",
            fill="#535353",
            font=("Roboto", 20 * -1)
        )
        
        canvas.create_rectangle(
            567.0,
            166.0,
            897.0,
            496.0,
            fill="#DDDDDD",
            outline="black")
        
        self.entry_code = ctk.CTkEntry(
            master=self,
            fg_color="#FFFFFF",
            width=467.0,
            height=82.0,
            text_color="black",
            font=ctk.CTkFont(size=48),
        )
        self.entry_code.place(
            x=42.0,
            y=166.0,
        )
        
        self.label = ttk.Label(self, text="Display")
        self.label.place(
            x=42.0,
            y=116.0
        )
        
        self.button_confirm = ctk.CTkButton(
            master=self,
            width=442,
            height=64,
            bg_color="#FFFFFF",
            border_width=1,
            text="Xác Nhận",
            text_color="white",
            font=ctk.CTkFont(size=24),
            command=lambda: verify_booking_code(self=self, input_data=self.entry_code.get()),
        )
        self.button_confirm.place(
            x=48.0,
            y=432.0,
        )
        
        self.button_back = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=lambda: controller.show_frame(MainScreen),
        )
        self.button_back.place(
            x=951.0,
            y=528.0,
        )
        
        button1 = tk.Button(self, text="Restart", command=lambda: self.restart(controller=controller))
        button1.pack()
        button2 = tk.Button(self, text="Refresh", command=self.refresh)
        button2.pack()
        
        self.keypad = Keypad(self)
        self.keypad.target = self.entry_code
        self.keypad.place(
            x=567,
            y=156,
        )
    
    def on_show_frame(self, event):
        if event:
            print("DeliveryScreen is being shown...")
    
    def restart(self, controller):
        self.refresh()
        controller.show_frame(MainScreen)
        
    def refresh(self):
        self.entry_code.delete(0, "end")
        self.label.configure(text="Display", foreground="black")

        
class PickupScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        entry_code_string = ""
        
        home_image = ctk.CTkImage(light_image=Image.open("assets/images/button_home.png"), size=[44, 44])
        back_image = ctk.CTkImage(light_image=Image.open("assets/images/button_back.png"), size=[44, 44])
        
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
        
        canvas.create_text(
            48.0,
            280.0,
            anchor="nw",
            text="Lưu ý: mã có thời hạn là 10 phút. Nếu mã hết hạn, \nhãy yêu cầu người nhận hàng gửi lại mã khác.",
            fill="#535353",
            font=("Roboto", 20 * -1)
        )
        
        canvas.create_text(
            568.0,
            108.0,
            anchor="nw",
            text="Nhập mã unlock tủ",
            fill="#535353",
            font=("Roboto", 20 * -1)
        )
        
        canvas.create_rectangle(
            567.0,
            166.0,
            897.0,
            496.0,
            fill="#DDDDDD",
            outline="black")
        
        entry_code = ctk.CTkEntry(
            master=self,
            fg_color="#FFFFFF",
            width=467.0,
            height=82.0,
            text_color="black",
            font=ctk.CTkFont(size=48),
            textvariable=entry_code_string,
        )
        entry_code.place(
            x=42.0,
            y=166.0,
        )
        
        self.button_confirm = ctk.CTkButton(
            master=self,
            width=442,
            height=64,
            bg_color="#FFFFFF",
            border_width=1,
            text="Xác Nhận",
            text_color="white",
            font=ctk.CTkFont(size=24),
            command=lambda: controller.show_frame(InstructionScreen),
        )
        self.button_confirm.place(
            x=48.0,
            y=432.0,
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
            command=lambda: controller.show_frame(MainScreen),
        )
        self.button_back.place(
            x=951.0,
            y=528.0,
        )
        
        self.keypad = Keypad(self)
        self.keypad.target = entry_code
        self.keypad.place(
            x=567,
            y=156,
        )
    
    def postupdate(self):
        self.entry.focus()

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
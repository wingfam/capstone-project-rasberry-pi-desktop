import customtkinter as ctk
from views.main_screen import MainScreen

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
        frame = MainScreen(container, self)
        self.frames[MainScreen] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainScreen)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    root = MainApp()
    root.mainloop()
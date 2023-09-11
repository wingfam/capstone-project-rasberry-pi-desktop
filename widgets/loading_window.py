import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

class LoadingWindow(tk.Toplevel):
    def __init__(self, parent, root):
        super().__init__()
        self.title("Đang xử lí")
        self.details_expanded = False
        
        # Removes the window's title bar
        self.overrideredirect(True)
        
        self.parent = parent
        self.root = root
        
        x = root.winfo_x()
        y = root.winfo_y()
        w = root.winfo_width()
        h = root.winfo_height()
        
        self.geometry("%dx%d+%d+%d" % (w/2, h/2, x + 256, y + 150))
        self.resizable(False, False)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.loadingLabel = ImageLabel(self)
        self.loadingLabel.load("assets/images/loading_roll.gif")
        self.loadingLabel.grid(row=1, column=1)
        
class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
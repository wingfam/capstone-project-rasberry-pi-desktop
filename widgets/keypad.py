import tkinter as tk
from tkinter import ttk

class Keypad(tk.Frame):

    cells = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['', '0', ''],
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = None
        
        style = ttk.Style()
        style.configure('my.TButton', font=('Helvetica', 20))

        for y, row in enumerate(self.cells):
            for x, item in enumerate(row):
                b = ttk.Button(
                    self, 
                    width=8,
                    style='my.TButton', 
                    text=item, 
                    command=lambda text=item:self.append(text)
                )
                b.grid(ipady=22, row=y, column=x, sticky='news')

        x = ttk.Button(self, text='Clear', command=self.clear)
        x.grid(ipady=22, row=3, column=0, sticky='news')
        
        x = ttk.Button(self, text='Backspace', command=self.backspace)
        x.grid(ipady=22, row=3, column=2, sticky='news')


    def get(self):
        if self.target:
            return self.target.get()

    def append(self, text):
        if self.target:
            self.target.insert('end', text)

    def clear(self):
        if self.target:
            self.target.delete(0, 'end')

    def backspace(self):
        if self.target:
            text = self.get()
            text = text[:-1]
            self.clear()
            self.append(text)
 
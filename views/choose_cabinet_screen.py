import sys
import os
import tkinter as tk
import customtkinter as ctk

from tkinter import StringVar
from constants.image_imports import home_image
from controllers.config_controller import DatabaseController


class ChooseCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.root = root
        
        self.databaseController = DatabaseController(view=self)

        self.chooseCabinet = StringVar()

        button_font = ctk.CTkFont(size=30, weight="bold")

        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text="",
            image=home_image,
            command=self.go_back_main_screen
        ).place(relx=.10, rely=.10, anchor=ctk.CENTER)

        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Add cabinet",
            command=self.go_to_add_screen
        ).place(relwidth=.25, relheight=.10, relx=.35, rely=.32, anchor=ctk.CENTER)

        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Check cabinet",
            command=self.go_to_check_cabinet
        ).place(relwidth=.25, relheight=.10, relx=.35, rely=.47, anchor=ctk.CENTER)

        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Restart",
            command=self.restart
        ).place(relwidth=.25, relheight=.10, relx=.35, rely=.62, anchor=ctk.CENTER)

        self.error_label = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=18),
            text_color="red",
            text="",
        )
        self.error_label.place(rely=.15, relx=.82, anchor="e")

        self.cabinetListBox = CabinetListBox(parent=self)
        self.cabinetListBox.place(rely=.45, relx=.75, anchor=ctk.CENTER)

    def set_cabinetId(self, name):
        results = self.databaseController.get_cabinet_by_name(name)
        for key, value in results.items():
            if key == 'id':
                self.root.cabinetId.set(value)
    
    def go_to_check_cabinet(self):
        cabinetName = self.root.cabinetName.get()
        if not cabinetName:
            self.error_label.configure(text="Please choose a cabinet")
        else:
            self.refresh()
            self.set_cabinetId(cabinetName)
            self.root.show_frame("ConfigScreen")

    def go_back_main_screen(self):
        self.refresh()
        self.root.show_frame("MainScreen")

    def go_to_add_screen(self):
        self.refresh()
        self.root.show_frame("AddCabinetScreen")

    def refresh(self):
        self.error_label.configure(text="")
        self.cabinetListBox.repopulate()

    def restart(self):
        '''Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function.'''
        # self.root.cleanAndExit()
        self.root.streamController.close_all_stream()
        python = sys.executable
        os.execl(python, python, * sys.argv)

class CabinetListBox(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.parent = parent

        self.listBox = tk.Listbox(
            master=self,
            font=ctk.CTkFont(size=24),
            justify=ctk.CENTER,
            background='white',
        )
        self.listBox.pack()

        cabinets = self.parent.databaseController.get_all_cabinet()
        self.insert_list_box(cabinets)

        self.listBox.bind("<<ListboxSelect>>", self.set_cabinet_name)

    def insert_list_box(self, cabinets):
        for key, value in cabinets.items():
            self.listBox.insert(key, value['name'])

    def set_cabinet_name(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.parent.root.cabinetName.set(data)

    def repopulate(self):
        self.listBox.delete(0, tk.END)
        cabinets = self.parent.databaseController.get_all_cabinet()
        self.insert_list_box(cabinets)

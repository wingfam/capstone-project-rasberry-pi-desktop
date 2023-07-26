import customtkinter as ctk
import tkinter as tk

from tkinter import ttk
from constants.image_imports import back_image
from controllers.config_controller import DatabaseController
from models.models import Box

# from controllers.control_gpio import ControlPinController
# from constants.gpio_constants import LoadCell, MageneticSwitch, SolenoidLock
# from models.models import Box


class ControlScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.parent = parent
        self.root = root
        self.boxModel = Box
        self.boxInfo = {}

        self.databaseController = DatabaseController(view=self)

        self.chooseBoxName = ctk.StringVar()
        self.lockStatus = ctk.StringVar(value="LOCK")
        self.switchStatus = ctk.StringVar(value="HIGH")
        self.weightValue = ctk.StringVar(value="0 GRAMS")

        button_font = ctk.CTkFont(size=24, weight="bold")

        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text="",
            image=back_image,
            command=self.go_back
        ).place(relx=.10, rely=.10, anchor=ctk.CENTER)

        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Lock/Unlock",
            command=self.lock_or_unlock_door
        ).place(relwidth=.20, relheight=.10, relx=.15, rely=.32, anchor=ctk.CENTER)

        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Check Switch",
            command=self.check_magnetic_switch
        ).place(relwidth=.20, relheight=.10, relx=.15, rely=.47, anchor=ctk.CENTER)

        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Check Weight",
            command=self.check_weight
        ).place(relwidth=.20, relheight=.10, relx=.15, rely=.62, anchor=ctk.CENTER)

        self.labelLockStatus = ttk.Entry(
            master=self,
            justify="center",
            state="disabled",
            background="white",
            font=ctk.CTkFont(size=24),
            textvariable=self.lockStatus,
        )

        self.labelSwitchStatus = ttk.Entry(
            master=self,
            justify="center",
            state="disabled",
            background="white",
            font=ctk.CTkFont(size=24),
            textvariable=self.switchStatus,
        )

        self.labelWeightValue = ttk.Entry(
            master=self,
            justify="center",
            state="disabled",
            background="white",
            font=ctk.CTkFont(size=24),
            textvariable=self.weightValue,
        )

        self.labelDisplay = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=20),
            bg_color='white',
            text="",
        )

        self.cabinetListBox = CabinetListBox(parent=self)

        self.labelLockStatus.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.32, anchor=ctk.CENTER)
        self.labelSwitchStatus.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.47, anchor=ctk.CENTER)
        self.labelWeightValue.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.62, anchor=ctk.CENTER)
        self.labelDisplay.place(
            relwidth=.20, relheight=.10, rely=.15, relx=.82, anchor="e")
        self.cabinetListBox.place(rely=.45, relx=.75, anchor=ctk.CENTER)

    def lock_or_unlock_door(self):
        if not self.chooseBoxName.get():
            self.labelDisplay.configure(
                text_color="red", text="Please choose a box")
        else:
            print(self.boxModel.id)
            print(self.boxModel.solenoidGpio)
            print(self.boxModel.switchGpio)
            print(self.boxModel.loadcellDout)
            print(self.boxModel.loadcellSck)

    def check_magnetic_switch(self):
        pass

    def check_weight(self):
        pass

    def refresh(self):
        self.labelDisplay.configure(text="")
        self.cabinetListBox.repopulate()

    def go_back(self):
        self.refresh()
        self.root.show_frame("ConfigScreen")


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

    def insert_list_box(self, cabinets):
        for key, value in cabinets.items():
            self.listBox.insert(key, value['nameBox'])

    def set_list_box(self):
        cabinetId = self.parent.root.cabinetId.get()
        boxes = self.parent.databaseController.get_box_by_cabinetId(cabinetId)
        self.insert_list_box(boxes)
        self.parent.boxInfo.update(boxes)
        self.listBox.bind("<<ListboxSelect>>", self.set_choice)

    def set_choice(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.parent.chooseBoxName.set(data)

        for key, value in self.parent.boxInfo.items():
            if value['nameBox'] == self.parent.chooseBoxName.get():
                self.parent.boxModel.id = value['id']
                self.parent.boxModel.solenoidGpio = value['solenoidGpio']
                self.parent.boxModel.switchGpio = value['switchGpio']
                self.parent.boxModel.loadcellDout = value['loadcellDout']
                self.parent.boxModel.loadcellSck = value['loadcellSck']

    def repopulate(self):
        self.listBox.delete(0, tk.END)
        cabinetId = self.parent.root.cabinetId.get()
        boxes = self.parent.databaseController.get_box_by_cabinetId(cabinetId)
        self.insert_list_box(boxes)

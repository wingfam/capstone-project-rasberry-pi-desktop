import customtkinter as ctk
import tkinter as tk

from tkinter import ttk
from constants.image_imports import back_image
from controllers.config_controller import DatabaseController, ManualControlController
from models.models import Box, SolenoidLock


class ControlScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.parent = parent
        self.root = root
        self.boxInfo = {}

        self.databaseController = DatabaseController(view=self)
        self.manualController = ManualControlController(view=self)

        self.boxModel = None
        self.solenoid = None

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

        self.button_on = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            fg_color="#1F6AA5",
            state=ctk.NORMAL,
            text="Unlock",
            command=self.unlock_door
        )

        self.button_off = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            fg_color="gray99",
            state=ctk.DISABLED,
            text="Lock",
            command=self.lock_door
        )

        ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Check Door",
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

        self.button_on.place(relwidth=.10, relheight=.10,
                             relx=.10, rely=.32, anchor=ctk.CENTER)
        self.button_off.place(relwidth=.10, relheight=.10,
                              relx=.20, rely=.32, anchor=ctk.CENTER)
        self.labelLockStatus.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.32, anchor=ctk.CENTER)
        self.labelSwitchStatus.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.47, anchor=ctk.CENTER)
        self.labelWeightValue.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.62, anchor=ctk.CENTER)
        self.labelDisplay.place(
            relwidth=.20, relheight=.10, rely=.15, relx=.82, anchor="e")
        self.cabinetListBox.place(rely=.45, relx=.75, anchor=ctk.CENTER)

    def define_gpio(self):
        solenoidPin = self.boxModel.solenoidGpio
        self.solenoid = self.manualController.set_LED(solenoidPin)

    def unlock_door(self):
        if not self.boxModel:
            self.labelDisplay.configure(
                text_color="red", text="Please choose a box")
        else:
            self.labelDisplay.configure(text="")
            self.button_on.configure(state=ctk.DISABLED, fg_color="gray99")
            self.button_off.configure(state=ctk.NORMAL, fg_color="#1F6AA5")

            self.manualController.unlock_door(self.solenoid)

    def lock_door(self):
        if not self.boxModel:
            self.labelDisplay.configure(
                text_color="red", text="Please choose a box")
        else:
            self.labelDisplay.configure(text="")
            self.button_on.configure(state=ctk.NORMAL, fg_color="#1F6AA5")
            self.button_off.configure(state=ctk.DISABLED, fg_color="gray99")

            self.manualController.lock_door(self.solenoid)

    def check_magnetic_switch(self):
        pass

    def check_weight(self):
        pass

    def refresh(self):
        self.boxModel = None
        self.solenoid = None
        self.labelDisplay.configure(text="")
        self.cabinetListBox.listBox.selection_clear(0, tk.END)
        self.cabinetListBox.listBox.delete(0, tk.END)

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
        self.parent.boxModel = Box
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

        self.parent.define_gpio()

    def repopulate(self):
        self.listBox.delete(0, tk.END)
        cabinetId = self.parent.root.cabinetId.get()
        boxes = self.parent.databaseController.get_box_by_cabinetId(cabinetId)
        self.insert_list_box(boxes)

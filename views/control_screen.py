import customtkinter as ctk
import tkinter as tk

from tkinter import ttk
from constants.image_imports import back_image
from controllers.config_controller import DatabaseController, ManualControlController
from models.models import Box, Gpio


class ControlScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.parent = parent
        self.root = root

        self.databaseController = DatabaseController(view=self)
        self.manualController = ManualControlController(view=self)

        self.gpioModel = None
        self.boxInfo = {}

        self.chooseBoxName = ctk.StringVar()
        self.lockStatus = ctk.StringVar(value="LOCK")
        self.switchStatus = ctk.StringVar()
        self.weightValue = ctk.StringVar()

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

        self.button_switch = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Check Door",
            command=self.check_magnetic_switch
        )

        self.button_weight = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Check Weight",
            command=self.check_package
        )

        self.labelLockStatus = ttk.Entry(
            master=self,
            justify="center",
            state="disabled",
            background="white",
            foreground="red",
            font=ctk.CTkFont(size=24),
            textvariable=self.lockStatus,
        )

        self.labelSwitchStatus = ttk.Entry(
            master=self,
            justify="center",
            state="disabled",
            background="white",
            foreground="black",
            font=ctk.CTkFont(size=24),
            textvariable=self.switchStatus,
        )

        self.labelWeightValue = ttk.Entry(
            master=self,
            justify="center",
            state="disabled",
            background="white",
            foreground="black",
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
        self.button_switch.place(
            relwidth=.20, relheight=.10, relx=.15, rely=.47, anchor=ctk.CENTER)
        self.button_weight.place(
            relwidth=.20, relheight=.10, relx=.15, rely=.62, anchor=ctk.CENTER)
        self.labelLockStatus.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.32, anchor=ctk.CENTER)
        self.labelSwitchStatus.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.47, anchor=ctk.CENTER)
        self.labelWeightValue.place(
            relwidth=.15, relheight=.10, relx=.40, rely=.62, anchor=ctk.CENTER)
        self.labelDisplay.place(
            relwidth=.20, relheight=.10, rely=.15, relx=.82, anchor="e")
        self.cabinetListBox.place(rely=.45, relx=.75, anchor=ctk.CENTER)

    def unlock_door(self):
        if not self.gpioModel:
            self.labelDisplay.configure(
                text_color="red", text="Please choose a box")
        else:
            self.lockStatus.set("UNLOCK")
            self.labelLockStatus.configure(foreground="green")
            self.labelDisplay.configure(text="")
            self.button_on.configure(state=ctk.DISABLED, fg_color="gray99")
            self.button_off.configure(state=ctk.NORMAL, fg_color="#1F6AA5")

            self.manualController.unlock_door(self.gpioModel.solenoid)

    def lock_door(self):
        if not self.gpioModel:
            self.labelDisplay.configure(
                text_color="red", text="Please choose a box")
        else:
            self.lockStatus.set("LOCK")
            self.labelLockStatus.configure(foreground="red")
            self.labelDisplay.configure(text="")
            self.button_on.configure(state=ctk.NORMAL, fg_color="#1F6AA5")
            self.button_off.configure(state=ctk.DISABLED, fg_color="gray99")

            self.manualController.lock_door(self.gpioModel.solenoid)

    def check_magnetic_switch(self):
        if not self.gpioModel:
            self.labelDisplay.configure(
                text_color="red", text="Please choose a box")
        else:
            self.labelDisplay.configure(text="")
            value = self.manualController.check_door(self.gpioModel.magSwitch)
            if not value:
                self.switchStatus.set("OPEN")
            else:
                self.switchStatus.set("CLOSE")

    def check_package(self):
        if not self.gpioModel:
            self.labelDisplay.configure(
                text_color="red", text="Please choose a box")
        else:
            self.labelDisplay.configure(text="")
            weight = self.manualController.check_weight(self.gpioModel.loadcell)
            self.weightValue.set(weight)

    def refresh(self):
        self.gpioModel = None
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
        boxId = None
        self.parent.gpioModel = Gpio
        selection = event.widget.curselection()
        
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.parent.chooseBoxName.set(data)
        
        for key, value in self.parent.boxInfo.items():
            if value['nameBox'] == self.parent.chooseBoxName.get():
                boxId = value['id']
                break
                
        for key, value in self.parent.root.globalBoxData.items():
            if value['id'] == boxId:
                self.parent.gpioModel.solenoid = value['solenoid']
                self.parent.gpioModel.magSwitch = value['magSwitch']
                self.parent.gpioModel.loadcell = value['loadcell']
                break
        
        if self.parent.gpioModel.solenoid.value() == 1:
            self.parent.lockStatus.set("UNLOCK")
            self.parent.button_on.configure(state=ctk.DISABLED, fg_color="gray99")
            self.parent.button_off.configure(state=ctk.NORMAL, fg_color="#1F6AA5")
        else:
            self.parent.lockStatus.set("LOCK")
            self.parent.button_on.configure(state=ctk.NORMAL, fg_color="#1F6AA5")
            self.parent.button_off.configure(state=ctk.DISABLED, fg_color="gray99")

    def repopulate(self):
        self.listBox.delete(0, tk.END)
        cabinetId = self.parent.root.cabinetId.get()
        boxes = self.parent.databaseController.get_box_by_cabinetId(cabinetId)
        self.insert_list_box(boxes)

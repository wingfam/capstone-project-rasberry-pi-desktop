import time
import customtkinter as ctk

from tkinter import IntVar
from constants.image_imports import back_image, refresh_image
from tkintertable import TableCanvas
from controllers.config_controller import AddCabinetController, DatabaseController, AddBoxController
from controllers.stream_controller import StreamController


class AddBoxScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)

        self.parent = parent
        self.controller = controller

        self.addBoxController = AddBoxController(view=self)
        self.databaseController = DatabaseController(view=self)
        self.streamController = StreamController(view=self.controller)

        self.cabinetId = ctk.StringVar()

        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text="",
            image=back_image,
            command=self.go_back,
        ).place(relx=.05, rely=.05, anchor=ctk.CENTER)

        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            font=ctk.CTkFont(size=24),
            text="",
        )
        self.display_label.place(
            relwidth=.53, relx=.45, rely=.05, anchor=ctk.CENTER)

        self.upload_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="2. Upload",
            state="disabled",
            command=self.upload_box
        )
        self.upload_button.place(
            relwidth=.35, relheight=.10, relx=.22, rely=.85, anchor=ctk.CENTER)

        self.add_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="1. Add box",
            command=self.add_box
        )
        self.add_button.place(relwidth=.35, relheight=.10,
                              relx=.75, rely=.85, anchor=ctk.CENTER)

        self.boxTable = BoxList(self, controller=self.controller)
        self.boxTable.place(relwidth=.90, relheight=.65,
                            relx=.48, rely=.45, anchor=ctk.CENTER)

    def add_box(self):
        tableData = self.boxTable.table.getModel().data
        isSaved = self.addBoxController.add_more_box(tableData)
        if isSaved:
            self.upload_button.configure(state="normal")

    def upload_box(self):
        tableData = self.boxTable.table.getModel().data
        # print("Data Length: ", len(tableData))
        self.controller.boxStream.close()

        isBoxUpload = self.addBoxController.upload_more_box(
            self.cabinetId.get(), len(tableData))

        if isBoxUpload:
            self.streamController.set_box_stream(self.cabinetId.get())
            self.upload_button.configure(state="disabled")
            newData = {
                '01': {
                    'nameBox': '',
                    'size': '',
                    'width': '',
                    'height': '',
                    'solenoidGpio': '',
                    'switchGpio': '',
                    'loadcellDout': '',
                    'loadcellSck': '',
                }
            }
            self.boxTable.table.model.importDict(newData)
            self.boxTable.table.redrawTable()

    def go_back(self):
        self.display_label.configure(text='')  # Clear display label
        self.controller.show_frame("ConfigScreen")


class BoxList(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)

        self.controller = controller
        self.parent = parent

        self.data = {
            '01': {
                'nameBox': '',
                'size': '',
                'width': '',
                'height': '',
                'solenoidGpio': '',
                'switchGpio': '',
                'loadcellDout': '',
                'loadcellSck': '',
            }
        }

        self.table = TableCanvas(
            parent=self,
            data=self.data,
            cellwidth=130,
            cellbackgr='#e3f698',
            thefont=('Arial', 12),
            rowheight=24,
            rowheaderwidth=30,
            read_only=False,
        )

        self.table.show()

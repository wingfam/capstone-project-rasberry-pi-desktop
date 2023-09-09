import os
import sys
import time
import customtkinter as ctk

from constants.image_imports import back_image
from tkintertable import TableCanvas
from controllers.config_controller import DatabaseController, AddBoxController
from controllers.stream_controller import StreamController


class AddBoxScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)

        self.parent = parent
        self.root = root

        self.addBoxController = AddBoxController(view=self)
        self.databaseController = DatabaseController(view=self)
        self.streamController = StreamController(view=self.root)

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

        self.add_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=30, weight="bold"),
            text="Save Box",
            command=self.save_box
        )

        self.boxTable = BoxList(self, root=self.root)
        self.boxTable.place(relwidth=.90, relheight=.65,relx=.48, rely=.45, anchor=ctk.CENTER)
        self.display_label.place(relwidth=.53, relx=.45, rely=.05, anchor=ctk.CENTER)
        self.add_button.place(relwidth=.55, relheight=.10, relx=.50, rely=.85, anchor=ctk.CENTER)

    def save_box(self):
        tableData = self.boxTable.table.getModel().data
        cabinetId = self.root.cabinetId.get()
        tableDataLen = len(tableData)
        
        isSaved = self.addBoxController.add_more_box(tableData)
        isTotalBoxUpdate = self.addBoxController.update_total_box(cabinetId)
        
        if isSaved and isTotalBoxUpdate:
            self.addBoxController.upload_more_boxes(cabinetId, tableDataLen)
            self.root.isRestart.set(True)

    def go_back(self):
        self.display_label.configure(text='')  # Clear display label
        self.root.show_frame("ConfigScreen")


class BoxList(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)

        self.root = root
        self.parent = parent

        self.data = {
            '01': {
                'nameBox': "",
                'solenoidGpio': 0,
                'switchGpio': 0,
                'loadcellDout': 0,
                'loadcellSck': 0,
                'loadcellRf': 0,
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

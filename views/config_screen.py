import os
import sys
import customtkinter as ctk

from tkinter import messagebox
from constants.image_imports import back_image
from controllers.config_controller import DatabaseController
from views.control_screen import ControlScreen
from views.edit_cabinet_screen import EditCabinetScreen


class ConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.root = root
        self.databaseController = DatabaseController(view=self)

        self.editScreen = EditCabinetScreen(
            parent=self, root=self.root)

        self.controlScreen = ControlScreen(
            parent=self, root=self.root)

        self.isRestart = False
        
        button_font = ctk.CTkFont(size=38, weight="bold")

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
        
        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text_color="red",
            font=ctk.CTkFont(size=24),
            text="",
        )

        self.edit_button = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Edit Info",
            command=self.go_to_edit_screen
        )

        self.add_box_button = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Add Box",
            command=self.go_to_add_box_screen
        )

        self.manual_control_button = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Manual Control",
            command=self.go_to_control_screen
        )
        
        self.delete_button = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Delete Cabinet",
            command=self.delete
        )
        
        
        self.edit_button.place(relwidth=.45, relheight=.15, relx=.5, rely=.20, anchor=ctk.CENTER)
        self.add_box_button.place(relwidth=.45, relheight=.15, relx=.5, rely=.40, anchor=ctk.CENTER)
        self.manual_control_button.place(relwidth=.45, relheight=.15, relx=.5, rely=.60, anchor=ctk.CENTER)
        self.delete_button.place(relwidth=.45, relheight=.15, relx=.5, rely=.80, anchor=ctk.CENTER)
        self.display_label.place(relwidth=.23, relx=.12, rely=.50, anchor=ctk.CENTER)
        

    def go_back(self):
        if not self.isRestart:
            self.root.show_frame("ChooseCabinetScreen")
        else:
            answer = messagebox.askyesno("Question","Bạn cần restart lại hệ thống trước")
            if answer:
                self.restart()

    def go_to_edit_screen(self):
        self.root.show_frame("EditCabinetScreen")

    def go_to_add_box_screen(self):
        self.root.show_frame("AddBoxScreen")

    def go_to_control_screen(self):
        self.root.show_frame("ControlScreen")

    def delete(self):
        answer = messagebox.askyesno("Question","Xóa Cabinet này?")
        if answer:
            cabinetName = self.root.cabinetName.get()
            cabinetId = self.root.cabinetId.get()
            isCabinetDeleted = self.databaseController.delete_cabinet(cabinetName)
            isCabinetLogDeleted = self.databaseController.delete_cabinetLog(cabinetId)
            isBoxDeleted = self.databaseController.delete_boxes(cabinetId)
        
            if not isCabinetDeleted and not isCabinetLogDeleted and not isBoxDeleted:
                return self.display_label.configure(text="Không thể xóa cabinet")
            else:
                self.isRestart = True
        
        if self.isRestart:
            answer = messagebox.askyesno("Question","Bạn cần restart lại hệ thống trước")
            if answer:
                self.restart()
        
    def refresh(self):
        self.display_label.configure(text="")
    
    def restart(self):
        '''Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function.'''
        # self.root.cleanAndExit()
        self.root.streamController.close_all_stream()
        python = sys.executable
        os.execl(python, python, * sys.argv)
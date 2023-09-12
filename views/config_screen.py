import os
import sys
import customtkinter as ctk

from tkinter import messagebox
from constants.image_imports import back_image
from controllers.config_controller import DatabaseController


class ConfigScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.root = root

        self.databaseController = DatabaseController(view=self)
        
        button_font = ctk.CTkFont(size=38, weight="bold")

        self.go_back_btn = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text="",
            image=back_image,
            command=self.go_back
        )
        
        self.edit_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Chỉnh sửa Cabinet",
            command=self.go_to_edit_screen
        )

        self.add_box_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Thêm hộp tủ",
            command=self.go_to_add_box_screen
        )
        
        self.manual_control_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Điều khiển thiết bị",
            command=self.go_to_control_screen
        )
        
        self.restart_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Khởi động lại",
            command=self.restart
        )
        
        self.go_back_btn.place(relx=.10, rely=.10, anchor=ctk.CENTER)
        self.edit_btn.place(relwidth=.45, relheight=.15, relx=.5, rely=.20, anchor=ctk.CENTER)
        self.add_box_btn.place(relwidth=.45, relheight=.15, relx=.5, rely=.40, anchor=ctk.CENTER)
        self.manual_control_btn.place(relwidth=.45, relheight=.15, relx=.5, rely=.60, anchor=ctk.CENTER)
        self.restart_btn.place(relwidth=.45, relheight=.15, relx=.5, rely=.80, anchor=ctk.CENTER)

    def restart(self):
        '''Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function.'''
        self.root.streamController.close_all_stream()
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def go_to_edit_screen(self):
        self.root.show_frame("EditCabinetScreen")

    def go_to_add_box_screen(self):
        self.root.show_frame("AddBoxScreen")
    
    def go_to_control_screen(self):
        self.root.show_frame("ControlScreen")
        
    def go_back(self):
        # print("Is Restart: ", self.root.isRestart.get())
        if not self.root.isRestart.get():
            self.root.show_frame("MainScreen")
        else:
            answer = messagebox.askyesno("Question", "Bạn cần restart lại hệ thống trước")
            if answer:
                self.restart()

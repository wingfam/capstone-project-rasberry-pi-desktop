import customtkinter as ctk

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

        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Edit Info",
            command=self.go_to_edit_screen
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.30, anchor=ctk.CENTER)

        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Add Box",
            command=self.go_to_add_box_screen
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.50, anchor=ctk.CENTER)

        self.control_screen_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Manual Control",
            command=self.go_to_control_screen
        ).place(relwidth=.45, relheight=.15, relx=.5, rely=.70, anchor=ctk.CENTER)

    def go_back(self):
        self.root.show_frame("ChooseCabinetScreen")

    def go_to_edit_screen(self):
        self.root.show_frame("EditCabinetScreen")

    def go_to_add_box_screen(self):
        self.root.show_frame("AddBoxScreen")

    def go_to_control_screen(self):
        self.root.show_frame("ControlScreen")

import os
import sys
import customtkinter as ctk

from tkinter import IntVar, messagebox
from constants.image_imports import back_image
from tkintertable import TableCanvas
from controllers.config_controller import AddCabinetController, DatabaseController, SetupController
from controllers.stream_controller import StreamController


class AddCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.parent = parent
        self.root = root
        
        self.databaseController = DatabaseController(view=self)
        self.addCabinetController = AddCabinetController(view=self)
        
        self.isRestart = False
        
        self.cabinetData = {}
        
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.totalBox = ctk.StringVar()
        self.businessId = ctk.StringVar()
        self.locationId = ctk.StringVar()
        self.locationName = ctk.StringVar()
        
        label_font = ctk.CTkFont(size=24)
        
        self.go_back_btn = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=self.go_back_prev_screen,
        )
        
        self.box_list_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=label_font,
            text="Box list: ",
        )
        
        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text_color="red",
            text="",
        )
        
        self.cabinet_name_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Tên tủ: ",
        )
        
        self.total_box_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Số hộp tủ: ",
        )
        
        self.cabinetName_entry = ctk.CTkEntry(
            master=self,
            width=100,
            fg_color="white",
            text_color="black",
            state="disabled",
            font=ctk.CTkFont(size=24),
            textvariable=self.cabinetName,
        )
        
        self.total_box_entry = ctk.CTkEntry(
            master=self,
            width=100,
            fg_color="white",
            text_color="black",
            state="disabled",
            font=ctk.CTkFont(size=24),
            textvariable=self.totalBox,
        )
        
        self.save_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Save Data",
            command=self.save_data
        )
        
        self.restart_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="Restart System",
            state="disabled",
            command=self.save_data
        )
        
        self.boxTable = BoxList(self, root=self.root)
        
        self.go_back_btn.place(relx=.05, rely=.10, anchor=ctk.CENTER)
        self.box_list_label.place(relx=.60, rely=.08, anchor=ctk.CENTER)
        self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        self.cabinet_name_label.place(relx=.08, rely=.25, anchor=ctk.CENTER)
        self.total_box_label.place(relx=.08, rely=.35, anchor=ctk.CENTER)
        self.cabinetName_entry.place(relwidth=.20, relx=.31, rely=.25, anchor=ctk.CENTER)
        self.total_box_entry.place(relwidth=.20, relx=.31, rely=.35, anchor=ctk.CENTER)
        self.save_button.place(relwidth=.35, relheight=.10, relx=.22, rely=.72, anchor=ctk.CENTER)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
    
    def save_data(self):
        tableData = self.boxTable.table.getModel().data
        isSave = self.addCabinetController.save_to_database()
        isUpload = self.addCabinetController.upload_to_firebase(len(tableData))
        self.restart_button.configure(state="normal")
        answer = None
        
        if isSave and isUpload:
            self.isRestart = True
            self.display_label.configure(text_color="green", text="Thông tin cabinet và box được tạo thành công")
            answer = messagebox.askyesno("Question","Cần restart lại hệ thống khi đã thêm thông tin")
        
        if answer:
            self.restart()
    
    def go_back_prev_screen(self):
        if not self.isRestart:
            self.refresh()
            self.root.show_frame("ChooseCabinetScreen")
        else:
            return self.display_label.configure(text_color="red", text="Bạn cần restart lại hệ thống trước")
    
    def restart(self):
        '''Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function.'''
        self.root.streamController.close_all_stream()
        python = sys.executable
        os.execl(python, python, * sys.argv)
    
    def refresh(self):
        self.boxTable.data.clear()
        tableData = self.boxTable.table.getModel().data
        tableData.clear()
   
    
class BoxList(ctk.CTkFrame):
    def __init__ (self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.root = root
        self.parent = parent
        
        self.data = {}
        
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
            
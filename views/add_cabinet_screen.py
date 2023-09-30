import os
import sys
from tkinter import messagebox

import customtkinter as ctk
from tkintertable import TableCanvas

from constants.image_imports import back_image
from controllers.config_controller import (AddCabinetController,
                                           DatabaseController)
from widgets.loading_window import LoadingWindow


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
        self.cabinetLogData = {}
        self.boxData = {}
        
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.totalBox = ctk.StringVar()
        self.masterCode = ctk.StringVar()
        self.businessId = ctk.StringVar()
        self.locationId = ctk.StringVar()
        
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
            text="Hộp tủ: ",
        )
        
        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text_color="red",
            text="",
        )
        
        self.name_label = ctk.CTkLabel(
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
            text="Số tủ: ",
        )
        
        self.master_code_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Mã master: ",
        )
        
        self.name_entry = ctk.CTkEntry(
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
        
        self.master_code_entry = ctk.CTkEntry(
            master=self,
            width=100,
            fg_color="white",
            text_color="black",
            state="disabled",
            font=ctk.CTkFont(size=24),
            textvariable=self.masterCode,
        )
        
        self.save_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="1. Lưu thông tin",
            command=self.do_save_data
        )
        
        self.restart_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=28, weight="bold"),
            text="2. Khởi động lại",
            state="disabled",
            command=self.restart
        )
        
        self.boxTable = BoxList(self, root=self.root)
        
        self.go_back_btn.place(relx=.10, rely=.10, anchor=ctk.CENTER)
        self.box_list_label.place(relx=.60, rely=.08, anchor=ctk.CENTER)
        self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        self.name_label.place(relx=.08, rely=.25, anchor=ctk.CENTER)
        self.total_box_label.place(relx=.08, rely=.35, anchor=ctk.CENTER)
        self.master_code_label.place(relx=.08, rely=.45, anchor=ctk.CENTER)
        self.name_entry.place(relwidth=.20, relx=.31, rely=.25, anchor=ctk.CENTER)
        self.total_box_entry.place(relwidth=.20, relx=.31, rely=.35, anchor=ctk.CENTER)
        self.master_code_entry.place(relwidth=.20, relx=.31, rely=.45, anchor=ctk.CENTER)
        self.save_button.place(relwidth=.30, relheight=.10, relx=.22, rely=.65, anchor=ctk.CENTER)
        self.restart_button.place(relwidth=.30, relheight=.10, relx=.22, rely=.78, anchor=ctk.CENTER)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
    
    def do_save_data(self):
        self.loadingWindow = LoadingWindow(self, self.root)
        self.loadingWindow.after(500, self.save_data_to_db)
    
    def save_data_to_db(self):
        try:
            self.save_button.configure(state="disabled")
            answer = None
            
            cabinetId = self.cabinetId.get()
            cabinetData = self.cabinetData
            cabinetLogData = self.cabinetLogData
            boxData = self.boxData
            tableData = self.boxTable.table.getModel().data
            # totalBox = len(tableData)
            
            if self.root.createBox.get():
                isBoxSaved = self.addCabinetController.create_boxes(tableData, cabinetId)
                self.addCabinetController.upload_boxes(cabinetId)
                # self.addCabinetController.update_cabinet_status(cabinetId)
            else:
                # self.addCabinetController.update_cabinet_status(cabinetId)
                isBoxSaved = self.addCabinetController.save_boxes(tableData, boxData, cabinetId)    
            
            isCabinetSaved = self.addCabinetController.save_cabinet(cabinetData)
            # isLogSaved = self.addCabinetController.save_cabinet_log(cabinetLogData)
            
            # self.addCabinetController.update_cabinet_status(cabinetId)
            # self.addCabinetController.update_box_status(cabinetId)
            
            if isCabinetSaved and isBoxSaved:
                self.isRestart = True
             
                self.addCabinetController.update_cabinet_status(cabinetId)
                self.addCabinetController.update_box_status(cabinetId)
                
                self.restart_button.configure(state="normal")
                self.save_button.configure(state='disabled')
                self.display_label.configure(text_color="green", text="Thông tin được lưu thành công")
                
        except Exception as e:
            print("Add cabinet error: ", e)
        finally:
            self.loadingWindow.destroy()
            self.save_button.after(1500, self.enable_save_button)
        
        answer = messagebox.askyesno("Question","Khởi động lại hệ thống?")
        if answer:
            self.refresh()
            self.restart()

    def enable_save_button(self):
        self.save_button.configure(state="normal")

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
        self.boxData.clear()
        self.restart_button.configure(state="disabled")
        self.save_button.configure(state='normal')
        self.boxTable.table.getModel().data.clear()
   
    
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
            
import os
import sys
import tkinter as tk
import customtkinter as ctk

from tkinter import IntVar, messagebox
from constants.image_imports import back_image
from tkintertable import TableCanvas
from controllers.config_controller import DatabaseController, EditCabinetController
from controllers.stream_controller import StreamController


class EditCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
        self.parent = parent
        self.root = root
        
        self.editController = EditCabinetController(view=self)
        self.databaseController = DatabaseController(view=self)
        self.streamController = StreamController(view=self.root)
        
        self.statusComboboxValues = ["Đã kích hoạt", "Chưa kích hoạt"]
        self.cabinetData = {}
        self.boxData = {}
        
        self.x = root.winfo_x()
        self.y = root.winfo_y()
        
        self.status = IntVar()
        
        self.cabinetId = ctk.StringVar()
        self.cabinetName = ctk.StringVar()
        self.locationId = ctk.StringVar()
        self.locationName = ctk.StringVar()
        self.statusComboboxVar = ctk.StringVar()
        
        self.go_back_btn = ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text= "",
            image=back_image,
            command=self.go_back,
        )
        
        self.box_list_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="w",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Hộp tủ: ",
        )
        
        self.cabinet_name_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Tên tủ: ",
        )
        
        self.status_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Trạng thái: ",
        )
        
        self.business_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Doanh nghiệp: ",
        )
        
        self.location_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=24),
            text="Địa điểm: ",
        )
        
        self.display_label = ctk.CTkLabel(
            master=self,
            width=200,
            fg_color="white",
            text="",
        )
        
        self.name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            fg_color="white",
            text_color="black",
            font=ctk.CTkFont(size=24),
            textvariable=self.cabinetName,
        )
        
        self.status_combobox = ctk.CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            font=ctk.CTkFont(size=24),
            state="readonly",
            values=self.statusComboboxValues,
            variable=self.statusComboboxVar,
            command=self.status_combobox_callback
        )
        
        self.business_name_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=20),
            text="",
        )
        
        self.location_name_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=ctk.CTkFont(size=20),
            text="",
        )
    
        self.save_button = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=30, weight="bold"),
            text="Cập nhật",
            command=self.update
        )
        
        self.delete_btn = ctk.CTkButton(
            master=self,
            corner_radius=15.0,
            font=ctk.CTkFont(size=30, weight="bold"),
            text="Xóa Cabinet",
            command=self.delete
        )
        
        self.boxTable = BoxList(self)
        
        self.new_canvas = tk.Canvas(self)
        
        self.go_back_btn.place(relx=.05, rely=.10, anchor=ctk.CENTER)
        self.box_list_label.place(relx=.60, rely=.08, anchor=ctk.CENTER)
        self.cabinet_name_label.place(relx=.08, rely=.25, anchor=ctk.CENTER)
        self.status_label.place(relx=.08, rely=.35, anchor=ctk.CENTER)
        self.business_label.place(relx=.08, rely=.45, anchor=ctk.CENTER)
        self.location_label.place(relx=.08, rely=.55, anchor=ctk.CENTER)
        self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
        self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=ctk.CENTER)
        self.status_combobox.place(relwidth=.23, relx=.31, rely=.35, anchor=ctk.CENTER)
        self.business_name_label.place(relx=.31, rely=.45, anchor=ctk.CENTER)
        self.location_name_label.place(relx=.31, rely=.55, anchor=ctk.CENTER)
        self.save_button.place(relwidth=.30, relheight=.10, relx=.25, rely=.73, anchor=ctk.CENTER)
        self.delete_btn.place(relwidth=.30, relheight=.10, relx=.25, rely=.85, anchor=ctk.CENTER)
        self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
        
      
    def update(self):
        try:
            self.save_button.configure(state="disabled")
            
            isCabinetUpdate = self.editController.update_cabinet_data(self.cabinetData)
            isBoxUpdate = self.editController.update_box_data()
            isLogUpdate = self.editController.save_cabinet_log()
            
            if isCabinetUpdate and isBoxUpdate and isLogUpdate:
                self.root.isRestart.set(True)
                self.root.cabinetName.set(self.cabinetName.get())
                self.editController.upload_box()
                self.editController.upload_cabinet(self.cabinetId.get())
                self.editController.upload_cabinetLog(self.cabinetId.get())
                self.display_label.configure(text_color='green', text='Thông tin được cập nhật thành công')
            else:
                self.display_label.configure(text_color='red', text='Thông tin không cập nhật thành công')
        except Exception as e:
            print("Update error: ", e)
        finally:
            self.save_button.after(1500, self.enable_save_button)
    
    def delete(self):
        title = "Xóa cabinet"
        message = "Bạn có muốn xóa cabinet này?"
        answer = messagebox.askyesno(title, message)
        
        if answer:
            cabinetName = self.cabinetName.get()
            cabinetId = self.cabinetId.get()
            boxData = self.boxData
            
            isCabinetDeleted = self.databaseController.delete_cabinet(cabinetName)
            isCabinetLogDeleted = self.databaseController.delete_cabinetLog(cabinetId)
            isBoxDeleted = self.databaseController.delete_boxes(cabinetId)
            
            if isCabinetDeleted and isCabinetLogDeleted and isBoxDeleted:
                self.editController.updateFb_cabinet_status(cabinetId)
                self.editController.updateFb_box_status(boxData)
                self.root.isRestart.set(True)
            else:
                return self.display_label.configure(text="Không thể xóa cabinet")
        
        if self.root.isRestart.get():
            answer = messagebox.askyesno("Question","Bạn cần restart lại hệ thống trước")
            if answer:
                self.restart()
    
    def restart(self):
        '''Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function.'''
        # self.root.streamController.close_all_stream()
        python = sys.executable
        os.execl(python, python, * sys.argv)
       
    def status_combobox_callback(self, choice):
        if choice == 'Đã kích hoạt':
            self.status.set(1)
        elif choice == 'Chưa kích hoạt':
            self.status.set(0)
        
        self.statusComboboxVar.set(choice)
        choice = self.statusComboboxVar.get()
        
        tableData = self.boxTable.table.getModel().data
        
        for value in tableData.values():
            if self.status.get():
                value['status'] = 1
            else:
                value['status'] = 0

    def enable_save_button(self):
        self.save_button.configure(state="normal")
    
    def refresh(self):
        self.cabinetName.set("")
        self.statusComboboxVar.set("")
        self.display_label.configure(text="") 
        self.boxTable.data.clear()
        tableData = self.boxTable.table.getModel().data
        tableData.clear()
    
    def go_back(self):
        self.refresh()
        self.root.show_frame("ConfigScreen")
   
class BoxList(ctk.CTkFrame):
    def __init__ (self, parent):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
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

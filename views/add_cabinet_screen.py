# import os
# import sys
# import customtkinter as ctk

# from tkinter import IntVar, messagebox
# from constants.image_imports import back_image
# from tkintertable import TableCanvas
# from controllers.config_controller import AddCabinetController, DatabaseController, SetupController
# from controllers.stream_controller import StreamController


# class AddCabinetScreen(ctk.CTkFrame):
#     def __init__(self, parent, root):
#         ctk.CTkFrame.__init__(self, parent)
#         ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
#         self.parent = parent
#         self.root = root
        
#         self.databaseController = DatabaseController(view=self)
#         self.addCabinetController = AddCabinetController(view=self)
#         self.streamController = StreamController(view=self)
        
#         self.statusComboboxValues = ["Yes", "No"]
#         self.locationComboboxValues = []
#         self.locationData = {}
        
#         self.isRestart = False
#         self.statusComboboxVar = ctk.StringVar()
#         self.cabinetId = ctk.StringVar()
#         self.cabinetName = ctk.StringVar()
#         self.cabinetStatus = IntVar()
#         self.cabinetLocation = ctk.StringVar()
#         self.businessId = ctk.StringVar()
#         self.locationId = ctk.StringVar()
        
#         label_font = ctk.CTkFont(size=24)
        
#         self.go_back_btn = ctk.CTkButton(
#             master=self,
#             width=44,
#             height=44,
#             bg_color="#FFFFFF",
#             fg_color="#FFFFFF",
#             text= "",
#             image=back_image,
#             command=self.go_back_prev_screen,
#         )
        
#         self.box_list_label = ctk.CTkLabel(
#             master=self,
#             width=200,
#             anchor="w",
#             text_color="black",
#             font=label_font,
#             text="Box list: ",
#         )
        
#         self.cabinet_name_label = ctk.CTkLabel(
#             master=self,
#             width=200,
#             anchor="e",
#             text_color="black",
#             font=label_font,
#             text="Cabinet name: ",
#         )
        
#         self.status_label = ctk.CTkLabel(
#             master=self,
#             width=200,
#             anchor="e",
#             text_color="black",
#             font=label_font,
#             text="Is Available: ",
#         )
        
#         self.location_label = ctk.CTkLabel(
#             master=self,
#             width=200,
#             anchor="e",
#             text_color="black",
#             font=label_font,
#             text="Location: ",
#         )
        
#         self.display_label = ctk.CTkLabel(
#             master=self,
#             width=200,
#             fg_color="white",
#             text_color="red",
#             text="",
#         )
        
#         self.name_entry = ctk.CTkEntry(
#             master=self,
#             width=200,
#             fg_color="white",
#             text_color="black",
#             font=label_font,
#             textvariable=self.cabinetName,
#         )
        
#         self.status_combobox = ctk.CTkComboBox(
#             master=self,
#             fg_color="white",
#             text_color="black",
#             dropdown_text_color="black",
#             dropdown_fg_color="white",
#             font=label_font,
#             state="readonly",
#             values=self.statusComboboxValues,
#             variable=self.statusComboboxVar,
#             command=self.status_combobox_callback
#         )
        
#         self.location_combobox = ctk.CTkComboBox(
#             master=self,
#             fg_color="white",
#             text_color="black",
#             dropdown_text_color="black",
#             dropdown_fg_color="white",
#             state="readonly",
#             font=label_font,
#             variable=self.cabinetLocation,
#             command=self.location_combobox_callback
#         )
        
#         self.save_button = ctk.CTkButton(
#             master=self,
#             corner_radius=15.0,
#             font=ctk.CTkFont(size=28, weight="bold"),
#             text="Save Data",
#             command=self.save_data
#         )
        
#         self.restart_button = ctk.CTkButton(
#             master=self,
#             corner_radius=15.0,
#             font=ctk.CTkFont(size=28, weight="bold"),
#             text="Restart System",
#             state="disabled",
#             command=self.save_data
#         )
        
#         self.boxTable = BoxList(self, root=self.root)
        
#         self.go_back_btn.place(relx=.05, rely=.10, anchor=ctk.CENTER)
#         self.box_list_label.place(relx=.60, rely=.08, anchor=ctk.CENTER)
#         self.cabinet_name_label.place(relx=.08, rely=.25, anchor=ctk.CENTER)
#         self.status_label.place(relx=.08, rely=.35, anchor=ctk.CENTER)
#         self.location_label.place(relx=.08, rely=.45, anchor=ctk.CENTER)
#         self.display_label.place(relwidth=.23, relx=.31, rely=.15, anchor=ctk.CENTER)
#         self.boxTable.place(relwidth=.52, relheight=.65, relx=.72, rely=.45, anchor=ctk.CENTER)
#         self.location_combobox.place(relwidth=.23, relx=.310, rely=.45, anchor=ctk.CENTER)
#         self.status_combobox.place(relwidth=.23, relx=.31, rely=.35, anchor=ctk.CENTER)
#         self.name_entry.place(relwidth=.23, relx=.31, rely=.25, anchor=ctk.CENTER)
#         self.save_button.place(relwidth=.35, relheight=.10, relx=.22, rely=.72, anchor=ctk.CENTER)
    
#     def save_data(self):
#         tableData = self.boxTable.table.getModel().data
#         isSave = self.addCabinetController.save_to_database()
#         isUpload = self.addCabinetController.upload_to_firebase(len(tableData))
#         self.restart_button.configure(state="normal")
#         if isSave and isUpload:
#             self.isRestart = True
#             self.display_label.configure(text_color="green", text="Thông tin cabinet và box được tạo thành công")
#             answer = messagebox.askyesno("Question","Cần restart lại hệ thống khi đã thêm thông tin")
#             if answer:
#                 self.restart()
    
#     def set_location_data(self):
#         results = self.databaseController.get_location_data()
#         self.locationData.update(results)
        
#         for key, value in self.locationData.items():
#             self.locationComboboxValues.append(value['locationName'])
        
#         return self.location_combobox.configure(require_redraw=True, values=self.locationComboboxValues,)

#     def refresh(self):
#         self.locationData.clear()
#         self.locationComboboxValues.clear()
#         self.cabinetName.set("")
#         self.statusComboboxVar.set("")
#         self.cabinetLocation.set("")
#         self.display_label.configure(text="")
#         self.location_combobox.set('')
      
#     def status_combobox_callback(self, choice):
#         if choice == 'Yes':
#             self.cabinetStatus.set(1)
#         elif choice == 'No':
#             self.cabinetStatus.set(0)
#         self.statusComboboxVar.set(choice)
#         choice = self.statusComboboxVar.get()
    
#     def location_combobox_callback(self, choice):
#         self.cabinetLocation.set(choice)
#         locationChoice = self.cabinetLocation.get()
#         for key, value in self.locationData.items():
#             if value['locationName'] == locationChoice:
#                 self.businessId.set(value['businessId'])
#                 self.locationId.set(value['locationId'])
#         # print(locationChoice)
#         # print("BussinesId: ", self.businessId.get())
#         # print("LocationId: ", self.locationId.get())
   
#     def go_back_prev_screen(self):
#         if not self.isRestart:
#             self.refresh()
#             self.root.show_frame("ChooseCabinetScreen")
#         else:
#             return self.display_label.configure(text_color="red", text="Bạn cần restart lại hệ thống trước")
    
#     def restart(self):
#         '''Restarts the current program.
#         Note: this function does not return. Any cleanup action (like
#         saving data) must be done before calling this function.'''
#         # self.root.cleanAndExit()
#         self.root.streamController.close_all_stream()
#         python = sys.executable
#         os.execl(python, python, * sys.argv)
    
    
# class BoxList(ctk.CTkFrame):
#     def __init__ (self, parent, root):
#         ctk.CTkFrame.__init__(self, parent)
#         ctk.CTkFrame.configure(self, fg_color="white", require_redraw=True)
        
#         self.root = root
#         self.parent = parent
        
#         self.data = {
#             'rec': {
#                 'nameBox': "",
#                 'solenoidGpio': 0,
#                 'switchGpio': 0,
#                 'loadcellDout': 0,
#                 'loadcellSck': 0,
#                 'loadcellRf': 0,
#             }
#         }
        
#         self.table = TableCanvas(
#             parent=self,
#             data=self.data,
# 			cellwidth=130,
#             cellbackgr='#e3f698',
# 			thefont=('Arial', 12),
#             rowheight=24, 
#             rowheaderwidth=30,
#             read_only=False,
#         )
        
#         self.table.show()
            
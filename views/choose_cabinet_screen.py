import tkinter as tk
from tkinter import StringVar

import customtkinter as ctk

from constants.image_imports import refresh_image
from controllers.config_controller import DatabaseController


class ChooseCabinetScreen(ctk.CTkFrame):
    def __init__(self, parent, root):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.root = root
        
        self.databaseController = DatabaseController(view=self)

        self.businessComboboxValues = []
        self.locationComboboxValues = []
        
        self.locationData = {}
        self.businessData = {}
        self.cabinetData = {}
        
        self.chooseCabinet = StringVar()
        self.businessId = ctk.StringVar()
        self.businessName = ctk.StringVar()
        self.locationId = ctk.StringVar()
        self.locationName = ctk.StringVar()
        
        button_font = ctk.CTkFont(size=30, weight="bold")
        label_font = ctk.CTkFont(size=24)

        ctk.CTkButton(
            master=self,
            width=44,
            height=44,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text="",
            image=refresh_image,
            command=self.reload
        ).place(relx=.10, rely=.10, anchor=ctk.CENTER)
        
        self.business_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Doanh nghiệp: ",
        )
        
        self.location_label = ctk.CTkLabel(
            master=self,
            width=200,
            anchor="e",
            text_color="black",
            font=label_font,
            text="Địa điểm: ",
        )
        
        self.business_combobox = ctk.CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            font=ctk.CTkFont(size=24),
            state="readonly",
            variable=self.businessName,
            command=self.business_combobox_callback
        )
        
        self.location_combobox = ctk.CTkComboBox(
            master=self,
            fg_color="white",
            text_color="black",
            dropdown_text_color="black",
            dropdown_fg_color="white",
            state="readonly",
            font=ctk.CTkFont(size=24),
            variable=self.locationName,
            command=self.location_combobox_callback
        )

        self.check_cabinet_btn = ctk.CTkButton(
            master=self,
            anchor=ctk.CENTER,
            font=button_font,
            text="Xem thông tin",
            command=self.go_to_check_cabinet
        )

        self.error_label = ctk.CTkLabel(
            master=self,
            font=ctk.CTkFont(size=18),
            text_color="red",
            text="",
        )
        
        self.cabinetListBox = CabinetListBox(parent=self)
        
        
        self.error_label.place(rely=.15, relx=.82, anchor="e")
        self.business_label.place(relx=.13, rely=.25, anchor=ctk.CENTER)
        self.location_label.place(relx=.13, rely=.35, anchor=ctk.CENTER)
        self.business_combobox.place(relwidth=.30, relx=.40, rely=.25, anchor=ctk.CENTER)
        self.location_combobox.place(relwidth=.30, relx=.40, rely=.35, anchor=ctk.CENTER)
        self.check_cabinet_btn.place(relwidth=.30, relheight=.10, relx=.40, rely=.65, anchor=ctk.CENTER)
        self.cabinetListBox.place(rely=.45, relx=.75, anchor=ctk.CENTER)

    def business_combobox_callback(self, choice):
        self.locationData.clear()
        self.locationComboboxValues.clear()
        self.locationName.set("")
        
        self.businessName.set(choice)
        for key, value in self.businessData.items():
            if value['businessName'] == choice:
                self.businessId.set(value['businessId'])
                
        self.set_location_data()
    
    def location_combobox_callback(self, choice):
        self.cabinetListBox.listBox.delete(0, tk.END)
        
        self.locationName.set(choice)
        for key, value in self.locationData.items():
            if value['locationName'] == choice:
                self.locationId.set(value['locationId'])
        
        self.set_cabinet_data()

    def set_business_data(self):
        results = self.databaseController.get_business_data()
        self.businessData.update(results)
       
        for key, value in self.businessData.items():
            self.businessComboboxValues.append(value['businessName'])
        
        return self.business_combobox.configure(require_redraw=True, values=self.businessComboboxValues,)

    def set_location_data(self):
        businessId = self.businessId.get()
        results = self.databaseController.get_location_by_businessId(businessId)
        self.locationData.update(results)
        
        for key, value in self.locationData.items():
            self.locationComboboxValues.append(value['locationName'])
        
        return self.location_combobox.configure(require_redraw=True, values=self.locationComboboxValues,)
    
    def set_cabinet_data(self):
        locationId = self.locationId.get()
        results = self.databaseController.get_cabinet_by_locationId(locationId)
        
        for key, value in results.items():
            cabinetDicts = {key: {'cabinetId': value['cabinetId'], 'cabinetName': value['cabinetName']}}
            self.cabinetData.update(cabinetDicts)
            self.cabinetListBox.listBox.insert(key, value['cabinetName'])
        
        return self.cabinetListBox.listBox.configure(background='white')
        
    def go_to_check_cabinet(self):
        cabinetName = self.root.cabinetName.get()
        if not cabinetName:
            self.error_label.configure(text="Please choose a cabinet")
        else:
            self.refresh()
            self.root.show_frame("AddCabinetScreen")

    def go_back_main_screen(self):
        self.refresh()
        self.root.show_frame("MainScreen")

    def refresh(self):
        self.error_label.configure(text="")
        self.businessData.clear()
        self.businessComboboxValues.clear()
        self.businessName.set("")
        self.locationData.clear()
        self.locationComboboxValues.clear()
        self.locationName.set("")
        self.cabinetListBox.listBox.delete(0, tk.END)
    
    def reload(self):
        self.refresh()
        self.set_business_data()

class CabinetListBox(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        ctk.CTkFrame.configure(self, fg_color="white")

        self.parent = parent
        
        self.listBox = tk.Listbox(
            master=self,
            font=ctk.CTkFont(size=24),
            justify=ctk.CENTER,
            background='grey',
        )

        self.listBox.bind("<<ListboxSelect>>", self.set_cabinet_name)
        self.listBox.pack()
        

    def set_cabinet_name(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        data = event.widget.get(index)
        
        for ckey, cvalue in self.parent.cabinetData.items():
            for selectkey in self.listBox.curselection():
                if ckey == selectkey:
                    self.parent.root.cabinetId.set(cvalue['cabinetId'])
                    self.parent.root.cabinetName.set(cvalue['cabinetName'])
                    
        # print(self.parent.root.cabinetId.get(), self.parent.root.cabinetName.get())
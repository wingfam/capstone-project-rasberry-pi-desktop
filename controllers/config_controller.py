import time
import tkinter as tk
import sqlite3 as sqlite3

from urllib.request import pathname2url
from constants.db_table import DbTable, db_file_name
from models.models import Cabinet
from services.auth import firebase_login
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory
from constants.db_table import db_file_name

check_weight_time = 3

class ChooseCabinetController():
    def __init__(self, view):
        self.view = view
    
    def get_all_cabinet(self):
        databaseController = DatabaseController(view=self.view)
        conn = databaseController.opendb(db_file_name)
        cabinetDict = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * From Cabinet")
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                cabinetDict.update(rowData)
        except Exception as e:
            print(e)
        
        return cabinetDict

class AddCabinetController():
    def __init__(self, view):
        self.view = view
        
    '''TODO: save cabinet info and box info to local database'''
    def save_to_database(self):
        tableModel = self.view.boxTable.table.getModel()
        records = tableModel.data
        
        cabinetModel = Cabinet
        cabinetModel.id = firebaseDB.generate_key()
        cabinetModel.name = self.view.cabinetName.get()
        cabinetModel.isAvailable = self.view.cabinetIsAvailable.get()
        cabinetModel.locationId = self.view.locationId.get()
        
        print(cabinetModel.name)
        for record in records.values():
            print(record)

        print("File has been save!")
        
    def upload_to_firebase(self):
        print("File has been uploaded!")
        
    def get_location_data(self):
        try:
            fb_login = firebase_login()
            fb_locations = firebaseDB.child("Location").get(fb_login["idToken"])
            for location in fb_locations.each():
                newKey = firebaseDB.generate_key()
                locationName = location.val()['name']
                locationId = location.val()['id']
                newData = {newKey: {'locationId': locationId, 'locationName': locationName}}
                self.view.locationData.update(newData)
                self.view.locationNames.append(locationName)
                
        except IndexError:
            print("Location doesn't exist")
           
        self.view.location_combobox.configure(require_redraw=True, values=self.view.locationNames)
    
    def get_box_by_cabinetId(self, cabinetId):
        databaseController = DatabaseController(view=self.view)
        conn = databaseController.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * From Box WHERE cabinetId = ?", (cabinetId))
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                self.view.boxTable.data.update(rowData)
                
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
            
        model = self.view.boxTable.table.model
        model.importDict(self.view.boxTable.data)
        self.view.boxTable.table.redraw()

class DatabaseController():
    def __init__(self, view):
        self.view = view
        self.my_stream = None
        
        self.conn = self.opendb(db_file_name)
        
        if self.conn:
            self.conn.close()
        else:
            print("Create new database")
            self.create_new_db(self.conn)
    
    def opendb(self, db_file_name):
        conn = None
        try:
            # Making a connection between sqlite3 database and Python Program
            dburi = 'file:{}?mode=rw'.format(pathname2url(db_file_name))
            conn = sqlite3.connect(dburi, uri=True)
        except sqlite3.OperationalError:
            print( "Database doesn't exist.\n")
            return False
        
        return conn
                
    def create_new_db(self, conn):
        tables = DbTable()
        try:
            conn = sqlite3.connect(db_file_name)
            cursor = conn.cursor()
            # Create new table
            for table in tables.tableList:
                cursor.execute(table)
                
        except sqlite3.DatabaseError as e:
            print(e)
        finally:
            conn.close()
            
        print("New database has been created.")

class ControlPinController():
    def __init__(self, model, view):
        self.view = view
        self.model = model
        
    # This gets called whenever the ON button is pressed
    def unlock_door(self):
        print("Box's door is unlocked")

        # Disable ON button, enable OFF button, and turn on LED
        self.view.button_on.config(state=tk.DISABLED, bg='gray64')
        self.view.button_off.config(state=tk.NORMAL, bg='gray99')
        
        self.model.solenoid.off()
        print(self.model.magSwitch.value)

    # This gets called whenever the OFF button is pressed
    def lock_door(self):
        print("Box's door is locked")

        # Disable OFF button, enable ON button, and turn off LED
        self.view.button_on.config(state=tk.NORMAL, bg='gray99')
        self.view.button_off.config(state=tk.DISABLED, bg='gray64')
        self.model.solenoid.on()
        print(self.model.magSwitch.value)
    
    def check_weight(self):
        count = 0
        weight_value = 0
        loadcell = self.model.loadcell
        
        # Loop check loadcell weight value every 3 seconds 
        while count < check_weight_time:
            weight_value = max(0, int(loadcell.get_weight(5)))
            print(weight_value)
            count += 1
            time.sleep(1)
            
        newText = str(weight_value) + " grams"
        self.view.weight_label.configure(text=newText)
        print("Check weight done!")

    def confirm(self):
        # Unlock box's door. Add wait for release event to magnetic switch
        # and check its state after 3 seconds
        self.unlock_door()
        isReleased = self.model.magSwitch.wait_for_release(3.0)

        if not isReleased:
            print('Magnetic switch is released: ', isReleased)
            self.lock_door()
        else:
            # Add when held event to the switch. If the switch is held for
            # a hold_time seconds, activate lock_door function (check pin 
            # declare for hold_time)
            print("Add event to magnetic switch")
            self.model.magSwitch.when_held = self.lock_door
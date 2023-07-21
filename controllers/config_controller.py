import time
import tkinter as tk
import sqlite3 as sqlite3
import random
import math

from datetime import datetime
from urllib.request import pathname2url
from constants.db_table import DbTable, db_file_name
from models.models import Cabinet, Box, MasterCode
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory
from constants.db_table import db_file_name

check_weight_time = 3

class ChooseCabinetController():
    def __init__(self, view):
        self.view = view
    
    
class AddCabinetController():
    def __init__(self, view):
        self.view = view
     
    def save_to_database(self):
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
        tableModel = self.view.boxTable.table.getModel()
        records = tableModel.data
        
        record = self.view.databaseController.find_cabinet_name(self.view.cabinetName.get())
        isFound = self.view.databaseController.check_exist_cabinet(record)
        
        if not isFound:
            return self.view.error_label.configure(text="Cabinet name has already existed")
        else:
            cabinetModel = Cabinet
            cabinetSave = self.view.databaseController.save_cabinet_to_db(cabinetModel, currentTime) # Save cabinet entries
            
            if not cabinetSave:
                return self.view.error_label.configure(text="Make sure all cabinet entries are filled in")
             
            self.view.databaseController.save_master_code_to_db() # Save master code entries
            
            for record in records.values(): # Save box entries
                boxModel = Box
                boxSave = self.view.databaseController.save_box_to_db(boxModel, record)
                if not boxSave:
                    return self.view.error_label.configure(text="Make sure all box entries are filled in") 
            
            return self.view.error_label.configure(text_color="green", text="New cabinet saved successful")
        
    def upload_to_firebase(self):
        self.upload_cabinet()
        self.upload_mastercode()
        self.upload_box()
    
    def upload_cabinet(self):
        try:
            cabinets = self.view.databaseController.get_last_cabinet()
            for cabinet in cabinets.values():
                cabinetRef = firebaseDB.child("Cabinet")
                fb_isAvailable = None
                
                if cabinet['isAvailable']:
                    fb_isAvailable = True
                elif not cabinet['isAvailable']:
                    fb_isAvailable = False
                    
                newData = {
                    cabinet['id']: {
                        'id': cabinet['id'],
                        'name': cabinet['name'],
                        'addDate': cabinet['addDate'],
                        'isAvailable': fb_isAvailable,
                        'locationId': cabinet['locationId']
                    }
                }
                
                cabinetRef.update(newData)
        except Exception as e:
            print("An error has occurred: ", e)
        
    def upload_mastercode(self):    
        try:
            mastercodes = self.view.databaseController.get_last_master_code()
            for mastercode in mastercodes.values():
                mastercodeRef = firebaseDB.child("MasterCode")
                fb_isAvailable = None
                
                if mastercode['isAvailable']:
                    fb_isAvailable = True
                elif not mastercode['isAvailable']:
                    fb_isAvailable = False
                    
                newData = {
                    mastercode['id']: {
                        'id': mastercode['id'],
                        'code': mastercode['code'],
                        'isAvailable': fb_isAvailable,
                        'cabinetId': mastercode['cabinetId']
                    }
                }
                
                mastercodeRef.update(newData)
        except Exception as e:
            print("An error has occurred: ", e)
    
    def upload_box(self):
        try:
            boxes = self.view.databaseController.get_box_by_cabinetId(1)
            for box in boxes.values():
                boxRef = firebaseDB.child("Box")
                fb_isAvailable = None
                fb_isStore = None
                
                if box['isAvailable']:
                    fb_isAvailable = True
                elif not box['isAvailable']:
                    fb_isAvailable = False
                
                if box['isStore']:
                    fb_isStore = True
                elif not box['isStore']:
                    fb_isStore = False
                    
                newData = {
                    box['id']: {
                        'id': box['id'],
                        'nameBox': box['nameBox'],
                        'size': box['size'],
                        'width': box['width'],
                        'height': box['height'],
                        'isStore': fb_isStore,
                        'isAvailable': fb_isAvailable,
                        'cabinetId': box['cabinetId']
                    }
                }
                
                boxRef.update(newData)
        except Exception as e:
            print("An error has occurred: ", e)
            
    def get_location_data(self):
        try:
            fb_locations = firebaseDB.child("Location").get()
            for location in fb_locations.each():
                newKey = firebaseDB.generate_key()
                locationName = location.val()['name']
                locationId = location.val()['id']
                newData = {newKey: {'locationId': locationId, 'locationName': locationName}}
                self.view.locationData.update(newData)
                self.view.locationComboboxValues.append(locationName)
                
        except IndexError:
            print("Location doesn't exist")
           
        self.view.location_combobox.configure(require_redraw=True, values=self.view.locationComboboxValues)
    
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
    
    def get_last_cabinet(self):
        conn = self.opendb(db_file_name)
        cabinetDict = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * FROM Cabinet ORDER BY id DESC LIMIT 1")
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                cabinetDict.update(rowData)
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        return cabinetDict
    
    def get_all_cabinet(self):
        conn = self.opendb(db_file_name)
        cabinetDict = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * FROM Cabinet")
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                cabinetDict.update(rowData)
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        return cabinetDict

    def get_all_cabinet_id(self):
        conn = self.opendb(db_file_name)
        dicts = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT id FROM Cabinet")
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                dicts.update(rowData)
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        return dicts

    def get_last_master_code(self):
        conn = self.opendb(db_file_name)
        cabinetDict = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * FROM MasterCode ORDER BY id DESC LIMIT 1")
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                cabinetDict.update(rowData)
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        return cabinetDict
    
    def get_all_master_code(self):
        conn = self.opendb(db_file_name)
        dicts = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * FROM MasterCode")
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                dicts.update(rowData)
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        return dicts

    def get_all_box(self):
        conn = self.opendb(db_file_name)
        dicts = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * FROM Box")
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                dicts.update(rowData)
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        return dicts
    
    def get_box_by_cabinetId(self, cabinetId):
        conn = self.opendb(db_file_name)
        dicts = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            results = cur.execute("SELECT * FROM Box WHERE cabinetId = ?", (cabinetId,))
            
            count = 0
            for row in results:
                rowData = {
                    str(count): row
                }
                count += 1
                dicts.update(rowData)
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
            
        return dicts
    
    def find_cabinet_name(self, cabinetName):
        conn = self.opendb(db_file_name)
        results = None
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            cur.execute("SELECT name FROM Cabinet WHERE name = ?", (cabinetName,))
            
            results = cur.fetchone()
            conn.commit()
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        return results
    
    def check_exist_cabinet(self, foundRecord):
        if foundRecord:
            return False
        else:
            return True
            
    def save_cabinet_to_db(self, model, currentTime):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            
            model.id = firebaseDB.generate_key()
            model.name = self.view.cabinetName.get()
            model.addDate = currentTime
            model.isAvailable = self.view.cabinetIsAvailable.get()
            model.locationId = self.view.locationId.get()
            
            if not model.name or not model.isAvailable or not model.locationId:
                return self.view.error_label.configure(text="Cabinet entries can't be empty")
            else:
                self.view.cabinetId = model.id
                cabinet = (model.id, model.name, model.addDate, model.isAvailable, model.locationId)
            
                sql = '''
                    INSERT INTO Cabinet (id, name, addDate, isAvailable, locationId)
                    VALUES (?, ?, ?, ?, ?)
                '''
            
                cur.execute(sql, cabinet)
                conn.commit()
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
            return False
        finally:
            conn.close()
            
        return True
        
    def save_box_to_db(self, model, record):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            
            model.id = firebaseDB.generate_key()
            model.nameBox = record['nameBox']
            model.size = record['size']
            model.width = record['width']
            model.height = record['height']
            model.isStore = 0
            model.isAvailable = 1
            model.solenoidGpio = record['solenoidGpio']
            model.switchGpio = record['switchGpio']
            model.loadcellDout = record['loadcellDout']
            model.loadcellSck = record['loadcellSck']
            model.cabinetId = self.view.cabinetId
            
            box = (model.id, model.nameBox, model.size, model.width, 
                   model.height, model.isStore, model.isAvailable, model.solenoidGpio, 
                   model.switchGpio, model.loadcellDout, model.loadcellSck, model.cabinetId)
            
            sql = '''
                INSERT INTO Box (id, nameBox, size, width, height, isStore, isAvailable, 
                    solenoidGpio, switchGpio, loadcellDout, loadcellSck, cabinetId)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            cur.execute(sql, box)
            conn.commit()
        except Exception as e:
            print("An error has occurred: ", e)
            return False
        finally:
            conn.close()
            
        return True

    def save_master_code_to_db(self):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            
            # generate random 6 digits
            digits = [i for i in range(0, 10)]
            randomDigits = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                randomDigits += str(digits[index])
            
            model = MasterCode
            model.id = firebaseDB.generate_key()
            model.code = randomDigits
            model.isAvailable = 1
            model.cabinetId = self.view.cabinetId
            
            mastercode = (model.id, model.code, model.isAvailable, model.cabinetId)
            
            sql = '''
                INSERT INTO MasterCode (id, code, isAvailable, cabinetId)
                VALUES (?, ?, ?, ?)
            '''
            
            cur.execute(sql, mastercode)
            conn.commit()
        except Exception as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
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
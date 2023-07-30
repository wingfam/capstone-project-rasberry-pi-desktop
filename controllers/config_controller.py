import time
import sqlite3 as sqlite3
import random
import math

from gpiozero import LED, Button
from services.hx711 import HX711
from datetime import datetime
from urllib.request import pathname2url
from constants.db_table import DbTable, db_file_name
from models.models import Cabinet, Box, MasterCode
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory
from constants.db_table import db_file_name

check_weight_time = 3


class GpioController():
    def __init__(self, view):
        self.view = view

        '''Declare host for remote GPIO Only use to control gpio remotely'''
        # self.gpio_factory = PiGPIOFactory(host='192.168.0.101') # NOTE: This is a thread

        '''Magnetic switch hold time'''
        self.hold_time = 3.0

    def set_solenoid(self, pin):
        solenoid = LED(pin, initial_value=True)
        return solenoid

    def set_mag_switch(self, pin):
        mag_switch = Button(pin, pull_up=True, bounce_time=0.2, hold_time=self.hold_time)
        return mag_switch

    def set_loadcell(self, dout, sck, ref):
        # Loadcell reference unit
        referenceUnit = ref
        
        loadcell = HX711(dout, sck)
        loadcell.set_reading_format("MSB", "MSB")
        loadcell.set_reference_unit(referenceUnit)
        
        self.reset_loadcell(loadcell)
        self.tare_loadcell(loadcell)
        self.powerDown_loadcell(loadcell)
        
        return loadcell
    
    def tare_loadcell(self, loadcell):
        loadcell.tare()
        print("Loadcell tare done!")

    def powerUp_loadcell(self, loadcell):
        loadcell.power_up()
        print("Loadcell power up done!")

    def powerDown_loadcell(self, loadcell):
        loadcell.power_down()
        print("Loadcell power down done!")

    def reset_loadcell(self, loadcell):
        loadcell.reset()
        print("Loadcell reset done!")
    
    def setup_gpio(self):
        results = self.view.databaseController.get_box_gpio()
        for box in results:
            boxData = {
                box['id']: {
                    'id': box['id'],
                    'nameBox': box['nameBox'],
                    'solenoid': self.set_solenoid(box['solenoidGpio']),
                    'magSwitch': self.set_mag_switch(box['switchGpio']),
                    'loadcell': self.set_loadcell(
                        box['loadcellDout'], 
                        box['loadcellSck'],
                        box['loadcellRf']
                        ),
                }
            }
            
            self.view.globalBoxData.update(boxData)
            

class AddCabinetController():
    def __init__(self, view):
        self.view = view

    def save_to_database(self):
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
        tableModel = self.view.boxTable.table.getModel()
        records = tableModel.data

        result = self.view.databaseController.get_cabinet_by_name(
            self.view.cabinetName.get())

        if result:
            return self.view.display_label.configure(text_color="red", text="Cabinet name has already existed")
        else:
            cabinetModel = Cabinet
            cabinetSave = self.view.databaseController.save_cabinet_to_db(
                cabinetModel, currentTime)  # Save cabinet entries

            if not cabinetSave:
                return self.view.display_label.configure(text_color="red", text="Make sure all cabinet entries are filled in")
            else:
                self.view.databaseController.save_master_code_to_db()  # Save master code entries

                for record in records.values():  # Save box entries
                    boxModel = Box
                    boxSave = self.view.databaseController.save_box_to_db(
                        boxModel, record)
                    if not boxSave:
                        return self.view.display_label.configure(text_color="red", text="Make sure all box entries are filled in")

        return self.view.display_label.configure(text_color="green", text="New cabinet saved successful")

    def upload_cabinet(self):
        isUpload = None
        try:
            data = self.view.databaseController.get_last_cabinet()
            for value in data.values():
                cabinetRef = firebaseDB.child("Cabinet")
                fb_isAvailable = None

                if value['isAvailable']:
                    fb_isAvailable = True
                elif not value['isAvailable']:
                    fb_isAvailable = False

                newData = {
                    value['id']: {
                        'id': value['id'],
                        'name': value['name'],
                        'addDate': value['addDate'],
                        'isAvailable': fb_isAvailable,
                        'locationId': value['locationId']
                    }
                }

                cabinetRef.update(newData)
                # set view cabinetId
                self.view.cabinetId = value['id']
                isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload

    def upload_mastercode(self, cabinetId):
        isUpload = None
        try:
            data = self.view.databaseController.get_last_master_code()
            for mastercode in data.values():
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
                isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload

    def upload_box(self, cabinetId):
        isUpload = None
        try:
            data = self.view.databaseController.get_box_by_cabinetId(cabinetId)
            for box in data.values():
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
                        'width': box['width'],
                        'height': box['height'],
                        'isStore': fb_isStore,
                        'isAvailable': fb_isAvailable,
                        'cabinetId': box['cabinetId']
                    }
                }

                boxRef.update(newData)
                isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload


class EditCabinetController():
    def __init__(self, view):
        self.view = view

    def set_location_id(self, location):
        for value in self.view.locationData.items():
            if value[1]['locationName'] == location:
                self.view.locationId.set(value[1]['locationId'])

    def set_location_data(self):
        results = self.view.databaseController.get_location_data()
        self.view.locationData.update(results)

        for key, value in self.view.locationData.items():
            self.view.locationComboboxValues.append(value['locationName'])

        self.view.location_combobox.configure(
            values=self.view.locationComboboxValues)

    def get_infos(self):
        self.view.cabinetData = self.view.databaseController.get_cabinet_by_name(
            self.view.root.cabinetName.get())

        self.view.cabinetId.set(self.view.cabinetData['id'])
        self.view.cabinetName.set(self.view.cabinetData['name'])
        self.view.isAvailable.set(self.view.cabinetData['isAvailable'])
        self.view.locationId.set(self.view.cabinetData['locationId'])

        if self.view.cabinetData['isAvailable'] == 0:
            self.view.statusComboboxVar.set('No')
        elif self.view.cabinetData['isAvailable'] == 1:
            self.view.statusComboboxVar.set('Yes')

        self.set_location_data()

        for key, value in self.view.locationData.items():
            if value['locationId'] == self.view.cabinetData['locationId']:
                self.view.cabinetLocation.set(value['locationName'])

        boxResults = self.view.databaseController.get_box_by_cabinetId(
            self.view.cabinetId.get())

        # Set data inside table with box results
        self.set_box_data(boxResults)
        self.view.boxData.update(boxResults)

    def set_box_data(self, boxResults):
        boxData = {}
        for key, value in boxResults.items():
            boxData.update({
                key: {
                    'nameBox': value['nameBox'],
                    'width': value['width'],
                    'height': value['height'],
                    'solenoidGpio': value['solenoidGpio'],
                    'switchGpio': value['switchGpio'],
                    'loadcellDout': value['loadcellDout'],
                    'loadcellSck': value['loadcellSck'],
                    'loadcellRf': value['loadcellRf'],
                }
            })

        model = self.view.boxTable.table.model
        model.importDict(boxData)
        self.view.boxTable.table.redraw()

    def update_cabinet_data(self):
        cabinetValue = {
            'name': self.view.cabinetName.get(),
            'isAvailable': self.view.isAvailable.get(),
            'locationId': self.view.locationId.get(),
            'id': self.view.cabinetId.get()
        }

        self.view.root.cabinetName.set(cabinetValue['name'])
        isUpdate = self.view.databaseController.update_cabinet_to_db(
            cabinetValue)
        return isUpdate

    def update_box_data(self):
        isUpdate = None
        boxData = self.view.boxData
        tableData = self.view.boxTable.table.getModel().data

        for tableDataKey, tableDataValue in tableData.items():
            for boxDataKey, boxDataValue in boxData.items():
                if tableDataKey == boxDataKey:
                    updateValue = {boxDataValue['id']: tableDataValue}
                    isUpdate = self.view.databaseController.update_box_internal(
                        updateValue)

        return isUpdate

    def reupload_cabinet(self):
        isUpload = None
        try:
            cabinetId = self.view.cabinetData['id']
            cabinetRef = firebaseDB.child("Cabinet/", cabinetId)
            fb_isAvailable = None

            if self.view.cabinetData['isAvailable']:
                fb_isAvailable = True
            elif not self.view.cabinetData['isAvailable']:
                fb_isAvailable = False

            newData = {
                'id': self.view.cabinetData['id'],
                'name': self.view.cabinetData['name'],
                'addDate': self.view.cabinetData['addDate'],
                'isAvailable': fb_isAvailable,
                'locationId': self.view.cabinetData['locationId']
            }

            cabinetRef.update(newData)
            isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload

    def reupload_box(self):
        isUpload = None
        try:
            boxData = self.view.boxTable.data
            for box in boxData.values():
                boxId = box['id']
                boxRef = firebaseDB.child("Box/", boxId)
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
                    'nameBox': box['nameBox'],
                    'width': box['width'],
                    'height': box['height'],
                    'isStore': fb_isStore,
                    'isAvailable': fb_isAvailable,
                }

                boxRef.update(newData)
                isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload


class AddBoxController():
    def __init__(self, view):
        self.view = view

    def set_cabinetId(self):
        self.view.cabinetData = self.view.databaseController.get_cabinet_by_name(
            self.view.root.cabinetName.get())

        self.view.cabinetId.set(self.view.cabinetData['id'])

    def check_entries(self, value):
        isCheck = None
        if (not value['nameBox'] or not value['width'] 
            or not value['height'] or not value['solenoidGpio'] 
            or not value['switchGpio'] or not value['loadcellDout'] 
            or not value['loadcellSck'] or not value['loadcellRf']):
            isCheck = False
        else:
            isCheck = True

        return isCheck

    def add_more_box(self, data):
        isSaved = None
        for key, value in data.items():
            isCheck = self.check_entries(value)
            if not isCheck:
                self.view.display_label.configure(
                    text_color="red",
                    text="Please make sure all entries are correct")
                break
            else:
                boxModel = Box
                isSaved = self.view.databaseController.save_box_to_db(
                    boxModel, value)
                if isSaved:
                    self.view.display_label.configure(
                        text_color="green",
                        text="Box added successful")

        return isSaved

    def upload_more_box(self, cabinetId, limit):
        isUpload = None
        try:
            results = self.view.databaseController.get_last_box_insert_by_cabinetId(
                cabinetId, limit)

            for data in results:
                boxRef = firebaseDB.child("Box")
                fb_isAvailable = None
                fb_isStore = None

                if data['isAvailable']:
                    fb_isAvailable = True
                elif not data['isAvailable']:
                    fb_isAvailable = False

                if data['isStore']:
                    fb_isStore = True
                elif not data['isStore']:
                    fb_isStore = False

                newData = {
                    data['id']: {
                        'id': data['id'],
                        'nameBox': data['nameBox'],
                        'width': data['width'],
                        'height': data['height'],
                        'isStore': fb_isStore,
                        'isAvailable': fb_isAvailable,
                        'cabinetId': data['cabinetId']
                    }
                }

                boxRef.update(newData)

            isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload


class DatabaseController():
    def __init__(self, view):
        self.view = view

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
            print("Database doesn't exist.\n")
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

    def get_location_data(self):
        newData = {}
        try:
            fb_locations = firebaseDB.child("Location").get()
            print(fb_locations)
            for location in fb_locations.each():
                newKey = firebaseDB.generate_key()
                locationName = location.val()['name']
                locationId = location.val()['id']
                newData.update(
                    {newKey: {'locationId': locationId, 'locationName': locationName}})
        except IndexError:
            print("Location doesn't exist")

        return newData

    def get_last_cabinet(self):
        conn = self.opendb(db_file_name)
        cabinetDict = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()

            results = cur.execute(
                "SELECT * FROM Cabinet ORDER BY id DESC LIMIT 1")

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

            results = cur.execute(
                "SELECT * FROM MasterCode ORDER BY id DESC LIMIT 1")

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

    def get_box_by_cabinetId(self, cabinetId):
        conn = self.opendb(db_file_name)
        dicts = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()

            sql = '''
                SELECT *
                FROM Box 
                WHERE cabinetId = ?
            '''

            results = cur.execute(sql, (cabinetId,))

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

    def get_box_gpio(self):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()

            sql = '''
                SELECT id, nameBox, solenoidGpio, switchGpio, 
                    loadcellDout, loadcellSck, loadcellRf
                FROM Box 
            '''

            cur.execute(sql)
            results = cur.fetchall()
            conn.commit()
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return results

    def get_last_box_insert_by_cabinetId(self, cabinetId, limit):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()

            sql = '''
                SELECT *
                FROM Box 
                WHERE cabinetId = ? 
                ORDER BY nameBox DESC
                LIMIT ?
            '''

            cur.execute(sql, (cabinetId, limit,))
            results = cur.fetchall()
            conn.commit()
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return results

    def get_cabinet_by_name(self, cabinetName):
        conn = self.opendb(db_file_name)
        results = None
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()

            sql = '''
                SELECT * 
                FROM Cabinet 
                WHERE name = ?
            '''

            cur.execute(sql, (cabinetName,))
            results = cur.fetchone()
            conn.commit()
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return results

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
                return self.view.display_label.configure(text="Cabinet entries can't be empty")
            else:
                self.view.cabinetId = model.id
                cabinet = (model.id, model.name, model.addDate,
                           model.isAvailable, model.locationId)

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
            model.width = record['width']
            model.height = record['height']
            model.isStore = 0
            model.isAvailable = 1
            model.solenoidGpio = record['solenoidGpio']
            model.switchGpio = record['switchGpio']
            model.loadcellDout = record['loadcellDout']
            model.loadcellSck = record['loadcellSck']
            model.loadcellRf = record['loadcellRf']
            model.cabinetId = self.view.cabinetId

            box = (model.id, model.nameBox, model.width,
                   model.height, model.isStore, model.isAvailable, model.solenoidGpio,
                   model.switchGpio, model.loadcellDout, model.loadcellSck, model.loadcellRf, model.cabinetId)

            sql = '''
                INSERT INTO Box (id, nameBox, width, height, isStore, isAvailable, 
                    solenoidGpio, switchGpio, loadcellDout, loadcellSck, loadcellRf, cabinetId)
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

            mastercode = (model.id, model.code,
                          model.isAvailable, model.cabinetId)

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

    def update_cabinet_to_db(self, data):
        isUpdate = None
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            model = (
                data['name'],
                data['isAvailable'],
                data['locationId'],
                data['id']
            )

            sql = ''' 
                UPDATE Cabinet
                SET name = ?,
                    isAvailable = ?,
                    locationId = ?
                WHERE id = ?
            '''

            cur.execute(sql, model)
            conn.commit()
            isUpdate = True
            print("Update cabinet successful")
        except Exception as e:
            isUpdate = False
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return isUpdate

    def update_master_code_patch_event(self, data):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            model = (
                data['code'],
                data['isAvailable'],
                data['id']
            )

            sql = ''' 
                UPDATE MasterCode
                SET code = ?,
                    isAvailable = ?
                WHERE id = ?
            '''

            cur.execute(sql, model)
            conn.commit()
            print("Update master code successful")
        except Exception as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()

    def update_box_patch_event(self, data):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            model = (
                data['nameBox'],
                data['size'],
                data['width'],
                data['height'],
                data['isAvailable'],
                data['isStore'],
                data['id']
            )

            sql = ''' 
                UPDATE Box
                SET nameBox = ?,
                    size = ?,
                    width = ?,
                    height = ?,
                    isAvailable = ?,
                    isStore = ?
                WHERE id = ?
            '''

            cur.execute(sql, model)
            conn.commit()
            print("Update box successful")
        except Exception as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()

    def update_box_internal(self, data):
        isUpdate = None
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            model = ()

            for key, value in data.items():
                model = (
                    value['nameBox'],
                    value['width'],
                    value['height'],
                    value['solenoidGpio'],
                    value['switchGpio'],
                    value['loadcellDout'],
                    value['loadcellSck'],
                    value['loadcellRf'],
                    key
                )

            sql = ''' 
                UPDATE Box
                SET nameBox = ?,
                    width = ?,
                    height = ?,
                    solenoidGpio = ?,
                    switchGpio = ?,
                    loadcellDout = ?,
                    loadcellSck = ?,
                    loadcellRf = ?
                WHERE id = ?
            '''

            cur.execute(sql, model)
            conn.commit()
            isUpdate = True
            print("Update box successful")
        except Exception as e:
            isUpdate = False
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return isUpdate


class ManualControlController():
    def __init__(self, view):
        self.view = view

    # This gets called whenever the UNLOCK button is pressed
    def unlock_door(self, solenoid):
        solenoid.off()

    # This gets called whenever the LOCK button is pressed
    def lock_door(self, solenoid):
        solenoid.on()

    # Check magnetic switch value and return it
    def check_door(self, switch):
        switchValue = switch.value
        return switchValue

    def check_weight(self, loadcell):
        count = 0
        weight_value = 0
        loadcell.power_up()
        time.sleep(0.01)
        # Loop check loadcell weight value every 3 seconds
        weight_value = max(0, int(loadcell.get_weight(5)))

        loadcell.power_down()
        print("Check weight done!")
        
        time.sleep(0.01)
        return weight_value

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

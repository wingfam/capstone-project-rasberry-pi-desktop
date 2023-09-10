import sqlite3 as sqlite3
import time
from gpiozero import LED, Button
from services.hx711 import HX711
from datetime import datetime
from tkinter import messagebox
from urllib.request import pathname2url

from constants.db_table import DbTable, db_file_name
from models.models import Box, Cabinet, CabinetLog
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory

import RPi.GPIO as GPIO


check_weight_time = 3


class SetupController():
    def __init__(self, view):
        self.view = view

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
        
        # Set loadcell reading format
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
    
    def setup_cabinet_data(self):
        results = self.view.databaseController.get_cabinetId_cabinetName()
        for value in results.values():
            self.view.cabinetId.set(value['id'])
            self.view.cabinetName.set(value['nameCabinet'])
    
    def setup_box_data(self):
        results = self.view.databaseController.get_box_gpio()
        for box in results:
            boxData = {
                box['id']: {
                    'id': box['id'],
                    'solenoid': self.set_solenoid(box['solenoidGpio']),
                    'magSwitch': self.set_mag_switch(box['switchGpio']),
                    'loadcell': self.set_loadcell(
                        box['loadcellDout'], 
                        box['loadcellSck'],
                        box['loadcellRf']),
                }
            }
            
            self.view.globalBoxData.update(boxData)
            

class AddCabinetController():
    def __init__(self, view):
        self.view = view

    def get_infos(self):
        cabinetId = self.view.root.cabinetId.get()
        self.view.cabinetData = self.get_cabinet_by_id(cabinetId)        
        self.view.boxData = self.get_box_by_cabinetId(cabinetId)
        self.view.cabinetLogData = self.get_cabinetLog_by_cabinetId(cabinetId)
        
        self.view.cabinetId.set(self.view.root.cabinetId.get())
        self.view.cabinetName.set(self.view.root.cabinetName.get())
        self.view.masterCode.set(self.view.cabinetData['masterCode'])
        
        if self.view.cabinetData['status']:
            self.view.status.set('Đã kích hoạt')
        else:
            self.view.status.set('Chưa kích hoạt')

        # Set data inside table with box results
        if self.view.boxData:
            self.view.root.createBox.set(False)
            self.set_box_data(self.view.boxData)
            self.view.boxTable.data.update(self.view.boxData)
        else:
            emptyData = {
                0: {
                'nameBox': "",
                'solenoidGpio': 0,
                'switchGpio': 0,
                'loadcellDout': 0,
                'loadcellSck': 0,
                'loadcellRf': 0,
                }
            }
            
            self.view.root.createBox.set(True)
            model = self.view.boxTable.table.model
            model.importDict(emptyData)
            self.view.boxTable.table.redraw()
            self.view.boxTable.data.update(emptyData)
        
    def get_cabinet_by_id(self, cabinetId):
        newData = {}
        try:
            fb_cabinets = firebaseDB.child("Cabinet").child(cabinetId).get()
            newData.update(fb_cabinets.val())
        except IndexError:
            print("Cabinet doesn't exist")

        return newData
    
    def get_box_by_cabinetId(self, cabinetId):
        newData = {}
        try:
            fb_boxes = firebaseDB.child("Box").order_by_child("cabinetId").equal_to(cabinetId).get()
            newData.update(fb_boxes.val())
        except IndexError:
            print("Box doesn't exist")
        
        return newData
    
    def get_cabinetLog_by_cabinetId(self, cabinetId):
        newData = {}
        try:
            fb_cabinetLog = firebaseDB.child("CabinetLog").order_by_child("cabinetId").equal_to(cabinetId).get()
            newData.update(fb_cabinetLog.val())
        except IndexError:
            print("CabinetLog doesn't exist")

        return newData
    
    def set_box_data(self, boxResults):
        boxData = {}
        for key, value in boxResults.items():
            boxData.update({
                key: {
                    'nameBox': value['nameBox'],
                    'solenoidGpio': 0,
                    'switchGpio': 0,
                    'loadcellDout': 0,
                    'loadcellSck': 0,
                    'loadcellRf': 0,
                }
            })

        model = self.view.boxTable.table.model
        model.importDict(boxData)
        self.view.boxTable.table.redraw()    
    
    def save_cabinet(self, cabinetData):
        model = Cabinet
        model.id = cabinetData['id']
        model.nameCabinet = cabinetData['nameCabinet']
        model.status = 1
        model.addDate = cabinetData['addDate']
        model.masterCode = cabinetData['masterCode']
        model.masterCodeStatus = cabinetData['masterCodeStatus']
        model.businessId = cabinetData['businessId']
        model.locationId = cabinetData['locationId']
        
        isSaved = self.view.databaseController.save_cabinet_to_db(model)
        
        return isSaved
    
    def save_boxes(self, tableData, boxData, cabinetId):
        isSaved = False
        for tableValue in tableData.values():
            model = Box
            for boxValue in boxData.values():
                model.id = boxValue['id']
                model.nameBox = boxValue['nameBox']
                model.status = boxValue['status']
                model.solenoidGpio = tableValue['solenoidGpio']
                model.switchGpio = tableValue['switchGpio']
                model.loadcellDout = tableValue['loadcellDout']
                model.loadcellSck = tableValue['loadcellSck']
                model.loadcellRf = tableValue['loadcellRf']
                model.cabinetId = cabinetId
            
                isSaved = self.view.databaseController.save_box_to_db(model)
        
        return isSaved
    
    def create_boxes(self, tableModel, cabinetId):
        isSaved = False
        for value in tableModel.values():
            model = Box
            model.id = firebaseDB.generate_key()
            model.nameBox = value['nameBox']
            model.status = 1
            model.solenoidGpio = value['solenoidGpio']
            model.switchGpio = value['switchGpio']
            model.loadcellDout = value['loadcellDout']
            model.loadcellSck = value['loadcellSck']
            model.loadcellRf = value['loadcellRf']
            model.cabinetId = cabinetId
            
            isSaved = self.view.databaseController.save_box_to_db(model)
        
        return isSaved
    
    def save_cabinet_log(self, cabinetLogData):
        isSaved = False
        for value in cabinetLogData.values():
            model = CabinetLog
            model.id = value['id']
            model.cabinetId = value['cabinetId']
            model.messageTitle = value['messageTitle']
            model.messageBody = value['messageBody']
            model.messageStatus = value['messageStatus']
            model.createDate = value['createDate']
            
            isSaved = self.view.databaseController.save_cabinetLog_to_db(model)
        
        return isSaved
    
    def upload_boxes(self, cabinetId):
        isUpload = False
        try:
            results = self.view.databaseController.get_box_by_cabinetId(cabinetId)
            
            for value in results.values():
                boxRef = firebaseDB.child("Box")

                newData = {
                    value['id']: {
                        'id': value['id'],
                        'nameBox': value['nameBox'],
                        'status': value['status'],
                        'cabinetId': value['cabinetId']
                    }
                }
                
                boxRef.update(newData)

            isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)
        
        return isUpload
    
    def update_cabinet_status_totalBox(self, cabinetId, totalBox):
        isUpdate = None
        try:
            cabinetRef = firebaseDB.child("Cabinet/", cabinetId)
            
            newData = {
                'status': 1,
                'totalBox': totalBox
            }
            
            cabinetRef.update(newData)
            isUpdate = True
        except Exception as e:
            isUpdate = False
            print("An error has occurred: ", e)
        
        return isUpdate


class EditCabinetController():
    def __init__(self, view):
        self.view = view

    def get_location_by_id(self, locationId):
        location = ""
        try:
            fb_location = firebaseDB.child("Location").order_by_child("id").equal_to(locationId).get().val()
            for value in fb_location.values():
                location = value['nameLocation']
        except Exception as e:
            print("get_location_by_id", e)
        
        return location

    def get_business_by_id(self, businessId):
        business = ""
        try:
            fb_location = firebaseDB.child("Business").order_by_child("id").equal_to(businessId).get().val()
            for value in fb_location.values():
                business = value['businessName']
        except Exception as e:
            print("get_business_by_id", e)
        
        return business

    def set_box_data(self, boxResults):
        boxData = {}
        for key, value in boxResults.items():
            boxData.update({
                key: {
                    'nameBox': value['nameBox'],
                    'status': value['status'],
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

    def get_infos(self):
        self.view.cabinetData = self.view.databaseController.get_cabinet_by_name(
            self.view.root.cabinetName.get())

        self.view.cabinetId.set(self.view.root.cabinetId.get())
        self.view.cabinetName.set(self.view.root.cabinetName.get())
        self.view.status.set(self.view.cabinetData['status'])

        businessName = self.get_business_by_id(self.view.cabinetData['businessId'])
        locationName = self.get_location_by_id(self.view.cabinetData['locationId'])
        
        if self.view.cabinetData['status'] == 0:
            self.view.statusComboboxVar.set('Chưa kích hoạt')
        elif self.view.cabinetData['status'] == 1:
            self.view.statusComboboxVar.set('Đã kích hoạt')
        
        boxResults = self.view.databaseController.get_box_by_cabinetId(self.view.cabinetId.get())

        self.view.business_name_label.configure(text=businessName)
        self.view.location_name_label.configure(text=locationName)
        
        # Set data inside table with box results
        self.set_box_data(boxResults)
        self.view.boxData.update(boxResults)

    def update_cabinet_data(self, data):
        model = {
            'nameCabinet': self.view.cabinetName.get(),
            'status': self.view.status.get(),
            'masterCode': data['masterCode'],
            'masterCodeStatus': data['masterCodeStatus'],
            'businessId': data['businessId'],
            'locationId': data['locationId'],
            'id': self.view.cabinetId.get()
        }
        
        isUpdate = self.view.databaseController.update_cabinet_to_db(model)
        return isUpdate

    def update_box_data(self):
        isUpdate = None
        boxData = self.view.boxData
        tableData = self.view.boxTable.table.getModel().data

        for tableDataKey, tableDataValue in tableData.items():
            for boxDataKey, boxDataValue in boxData.items():
                if tableDataKey == boxDataKey:
                    updateValue = {boxDataValue['id']: tableDataValue}
                    isUpdate = self.view.databaseController.update_box_internal(updateValue)

        return isUpdate
    
    def save_cabinet_log(self):
        isUpdate = None
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M")
        
        model = CabinetLog
        model.id = firebaseDB.generate_key()
        model.messageTitle = "Cập nhật Cabinet"
        model.messageBody = "" + self.view.cabinetName.get() + " được cập nhật vào ngày: " + currentTime
        model.messageStatus = 1
        model.createDate = currentTime
        model.cabinetId = self.view.cabinetId.get()
        
        isSave = self.view.databaseController.save_cabinetLog_to_db(model)
        
        if isSave:
            isUpdate = True
        
        return isUpdate
        
    def upload_cabinet(self):
        isUpload = None
        try:
            cabinetId = self.view.cabinetId.get()
            cabinetRef = firebaseDB.child("Cabinet").child(cabinetId)
            
            newData = {
                'id': self.view.cabinetId.get(),
                'nameCabinet': self.view.cabinetName.get(),
                'status': self.view.status.get(),
                'businessId': self.view.businessId.get(),
                'locationId': self.view.locationId.get()
            }

            cabinetRef.update(newData)
            isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload

    def upload_box(self):
        isUpload = None
        try:
            boxData = self.view.boxData
            tableData = self.view.boxTable.table.getModel().data

            for tableDataKey, tableDataValue in tableData.items():
                for boxDataKey, boxDataValue in boxData.items():
                    if tableDataKey == boxDataKey:
                        boxDataValue['nameBox'] = tableDataValue['nameBox']
                        boxDataValue['status'] = tableDataValue['status']
                        
            for box in boxData.values():
                boxId = box['id']
                boxRef = firebaseDB.child("Box").child(boxId)

                newData = {
                    'nameBox': box['nameBox'],
                    'status': box['status']
                }

                boxRef.update(newData)
                isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload
    
    def upload_cabinetLog(self, cabinetId):
        isUpload = None
        try:
            data = self.view.databaseController.get_cabinetLog_by_cabinetId(cabinetId)
            for log in data.values():
                logRef = firebaseDB.child("CabinetLog")

                newData = {
                    log['id']: {
                        'id': log['id'],
                        'messageTitle': log['messageTitle'],
                        'messageBody': log['messageBody'],
                        'messageStatus': log['messageStatus'],
                        'createDate': log['createDate'],
                        'cabinetId': log['cabinetId']
                    }
                }

                logRef.update(newData)
                isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload

    def updateFb_cabinet_status(self, cabinetId):
        isUpdated = None
        try:
            cabinetRef = firebaseDB.child("Cabinet").child(cabinetId)
            
            newData = {
                'status': 0,
            }

            cabinetRef.update(newData)
            isUpdated = True
        except Exception as e:
            isUpdated = False
            print("An error has occurred: ", e)

        return isUpdated

    def updateFb_box_status(self, boxData):
        isUpdated = None
        try:
            for value in boxData.values():
                boxId = value['id']
                boxRef = firebaseDB.child("Box").child(boxId)

                newData = {
                    'status': 0
                }

                boxRef.update(newData)
                isUpdated = True
        except Exception as e:
            isUpdated = False
            print("An error has occurred: ", e)

        return isUpdated

class AddBoxController():
    def __init__(self, view):
        self.view = view

    def check_entries(self, value):
        isCheck = False
        if (not value['nameBox'] or not value['solenoidGpio'] 
            or not value['switchGpio']  or not value['loadcellDout'] 
            or not value['loadcellSck'] or not value['loadcellRf']):
            # print(value)
            isCheck = False
        else:
            isCheck = True

        return isCheck

    def add_more_box(self, data):
        isSaved = False
        
        for value in data.values():
            isCheck = self.check_entries(value)
            if not isCheck:
                self.view.display_label.configure(
                    text_color="red",
                    text="Hãy kiểm tra lại các ô điền đúng"
                )
                break
            else:
                # print("Save box data: ", value)
                isSaved = self.view.databaseController.save_box_to_db(value)
                if isSaved:
                    self.view.display_label.configure(
                        text_color="green",
                        text="Hộp tủ được tạo thành công")

        return isSaved

    def upload_more_boxes(self, cabinetId, limit):
        isUpload = False
        try:
            results = self.view.databaseController.get_last_box_insert_by_cabinetId(cabinetId, limit)

            for data in results:
                boxRef = firebaseDB.child("Box")

                newData = {
                    data['id']: {
                        'id': data['id'],
                        'nameBox': data['nameBox'],
                        'status': data['status'],
                        'cabinetId': data['cabinetId']
                    }
                }
                
                print(newData)

                boxRef.update(newData)

            isUpload = True
        except Exception as e:
            isUpload = False
            print("An error has occurred: ", e)

        return isUpload
    
    def update_total_box(self, cabinetId):
        isUpdate = None
        try:
            cabinetRef = firebaseDB.child("Cabinet/", cabinetId)
            boxResult = self.view.databaseController.get_box_by_cabinetId(cabinetId)
            totalBox = len(boxResult)
            
            newData = {
                'totalBox': totalBox
            }
            
            cabinetRef.update(newData)
            isUpdate = True
        except Exception as e:
            isUpdate = False
            print("An error has occurred: ", e)
        
        return isUpdate


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

    def get_business_data(self):
        newData = {}
        try:
            fb_business = firebaseDB.child("Business").get()
            
            newKey = 0
            for business in fb_business.each():
                businessId = business.val()['id']
                businessName = business.val()['businessName']
                businessStatus =  business.val()['status']
                
                if businessStatus == 1:
                    newData.update({
                        newKey: {
                            'businessId': businessId, 
                            'businessName': businessName,
                        }
                    })
                
                newKey += 1
        except IndexError:
            print("Location doesn't exist")

        return newData

    def get_location_by_businessId(self, businessId):
        newData = {}
        try:
            fb_locations = firebaseDB.child("Location").order_by_child("businessId").equal_to(businessId).get()
            
            newKey = 0
            for location in fb_locations.each():
                businessId = location.val()['businessId']
                locationName = location.val()['nameLocation']
                locationId = location.val()['id']
                
                newData.update({
                    newKey: {
                        'businessId': businessId, 
                        'locationId': locationId, 
                        'locationName': locationName
                    }
                })
                
                newKey += 1
                
        except IndexError:
            print("Location doesn't exist")

        return newData

    def get_cabinetId_cabinetName(self):
        conn = self.opendb(db_file_name)
        cabinetDict = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            sql = '''
                SELECT id, nameCabinet 
                FROM Cabinet
            '''
            
            results = cur.execute(sql)

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

    def get_cabinet_by_locationId(self, locationId):
        newData = {}
        try:
            fb_cabinets = firebaseDB.child("Cabinet").order_by_child("locationId").equal_to(locationId).get()
            
            newKey = 0
            for cabinet in fb_cabinets.each():
                id = cabinet.val()['id']
                name = cabinet.val()['nameCabinet']
                status = cabinet.val()['status']
                
                newData.update({
                    newKey: {
                        'cabinetId': id, 
                        'cabinetName': name,
                        'cabinetStatus': status
                    }
                })
                
                newKey += 1
                
        except IndexError:
            print("Location doesn't exist")

        return newData
    
    def get_masterCode(self, input):
        conn = self.opendb(db_file_name)
        dicts = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            
            sql = '''
                SELECT masterCode, masterCodeStatus
                FROM Cabinet 
                WHERE masterCode = ?
            '''
            
            results = cur.execute(sql, (input,))
            
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

    def get_cabinetLog_by_cabinetId(self, cabinetId):
        conn = self.opendb(db_file_name)
        dicts = {}
        try:
            conn = sqlite3.connect(db_file_name)
            conn.row_factory = dict_factory
            cur = conn.cursor()

            sql = '''
                SELECT *
                FROM CabinetLog 
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
                WHERE nameCabinet = ?
            '''

            cur.execute(sql, (cabinetName,))
            results = cur.fetchone()
            conn.commit()
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
        finally:
            conn.close()
        
        return results

    def save_cabinet_to_db(self, model):
        isSave = False
        conn = self.opendb(db_file_name)
        
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            cabinet = (
                model.id, 
                model.nameCabinet, 
                model.addDate, 
                model.status, 
                model.masterCode, 
                model.masterCodeStatus, 
                model.businessId,
                model.locationId
            )
            
            sql = '''
                INSERT INTO Cabinet (
                    id, nameCabinet, addDate, status, 
                    masterCode, masterCodeStatus, 
                    businessId, locationId)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''

            cur.execute(sql, cabinet)
            conn.commit()
            isSave = True
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
            isSave = False
        finally:
            conn.close()

        return isSave

    def save_cabinetLog_to_db(self, model):
        isSave = False
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            cabinetLog = (
                model.id, 
                model.messageTitle, 
                model.messageBody, 
                model.messageStatus, 
                model.createDate, 
                model.cabinetId
            )
            
            sql = '''
                INSERT INTO CabinetLog (
                    id, messageTitle, 
                    messageBody, messageStatus, 
                    createDate, cabinetId)
                VALUES (?, ?, ?, ?, ?, ?)
            '''

            cur.execute(sql, cabinetLog)
            conn.commit()
            isSave = True
        except conn.DatabaseError as e:
            print("An error has occurred: ", e)
            isSave = False
        finally:
            conn.close()

        return isSave
    
    def save_box_to_db(self, model):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            box = (
                model.id, 
                model.nameBox, 
                model.status,
                model.solenoidGpio, 
                model.switchGpio, 
                model.loadcellDout, 
                model.loadcellSck, 
                model.loadcellRf,
                model.cabinetId
            )

            sql = '''
                INSERT INTO Box (id, nameBox, status, 
                    solenoidGpio, switchGpio, loadcellDout, 
                    loadcellSck, loadcellRf, cabinetId)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            cur.execute(sql, box)
            conn.commit()
        except Exception as e:
            print("An error has occurred: ", e)
            return False
        finally:
            conn.close()

        return True

    def update_cabinet_to_db(self, data):
        isUpdate = None
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            model = (
                data['nameCabinet'],
                data['status'],
                data['masterCode'],
                data['masterCodeStatus'],
                data['businessId'],
                data['locationId'],
                data['id']
            )

            sql = ''' 
                UPDATE Cabinet
                SET nameCabinet = ?,
                    status = ?,
                    masterCode = ?,
                    masterCodeStatus = ?,
                    businessId = ?,
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

    def update_box_patch_event(self, data):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            model = (
                data['nameBox'],
                data['status'],
                data['id']
            )

            sql = ''' 
                UPDATE Box
                SET nameBox = ?,
                    status = ?
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
                    value['status'],
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
                    status = ?,
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
    
    def update_box_status(self, status, boxId):
        isUpdate = None
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            model = (status, boxId)

            sql = ''' 
                UPDATE Box
                SET status = ?,
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

    def delete_cabinet(self, nameCabinet):
        isDelete = None
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            model = (nameCabinet,)
            
            sql = ''' 
                DELETE FROM Cabinet
                WHERE nameCabinet = ?
            '''

            cur.execute(sql, model)
            conn.commit()
            isDelete = True
            print("Cabinet delete successful")
        except Exception as e:
            isDelete = False
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return isDelete
    
    def delete_boxes(self, cabinetId):
        isDelete = None
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            model = (cabinetId,)
            
            sql = ''' 
                DELETE FROM Box
                WHERE cabinetId = ?
            '''

            cur.execute(sql, model)
            conn.commit()
            isDelete = True
            print("Cabinet delete successful")
        except Exception as e:
            isDelete = False
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return isDelete
    
    def delete_cabinetLog(self, cabinetId):
        isDelete = None
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            model = (cabinetId,)
            
            sql = ''' 
                DELETE FROM CabinetLog
                WHERE cabinetId = ?
            '''

            cur.execute(sql, model)
            conn.commit()
            isDelete = True
            print("Cabinet delete successful")
        except Exception as e:
            isDelete = False
            print("An error has occurred: ", e)
        finally:
            conn.close()

        return isDelete
    

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

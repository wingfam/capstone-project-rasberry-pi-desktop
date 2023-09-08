import time
import sqlite3 as sqlite3
import random
import math
# import RPi.GPIO as GPIO

# from gpiozero import LED, Button
# from services.hx711 import HX711
from datetime import datetime
from urllib.request import pathname2url
from constants.db_table import DbTable, db_file_name
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory
from constants.db_table import db_file_name

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
        for key, value in results.items():
            self.view.cabinetId.set(value['id'])
            self.view.cabinetName.set(value['nameCabinet'])
    
    def setup_box_data(self):
        results = self.view.databaseController.get_box_gpio()
        for box in results:
            boxData = {
                box['id']: {
                    'id': box['id'],
                    # 'solenoid': self.set_solenoid(box['solenoidGpio']),
                    # 'magSwitch': self.set_mag_switch(box['switchGpio']),
                    # 'loadcell': self.set_loadcell(
                    #     box['loadcellDout'], 
                    #     box['loadcellSck'],
                    #     box['loadcellRf']),
                }
            }
            
            self.view.globalBoxData.update(boxData)
            

class AddCabinetController():
    def __init__(self, view):
        self.view = view

    def save_to_database(self):
        tableModel = self.view.boxTable.table.getModel()
        records = tableModel.data
        isSave = False

        result = self.view.databaseController.get_cabinet_by_name(self.view.cabinetName.get())

        if result is not None:
            return self.view.display_label.configure(text_color="red", text="Tên cabinet đã tồn tại")
        else:
            # Save cabinet entries
            cabinetSave = self.view.databaseController.save_cabinet_to_db()

            if not cabinetSave:
                return self.view.display_label.configure(text_color="red", text="Thông tin cabinet không thể lưu")
            else:
                # Save cabinet log
                logTitle = "Tạo cabinet"
                logMessage = "Cabinet mới được tạo"
                self.view.databaseController.save_cabinetLog_to_db(logTitle, logMessage, self.view.cabinetId)
                for record in records.values():
                    # Save box entries
                    boxSave = self.view.databaseController.save_box_to_db(record)
                    if not boxSave:
                        return self.view.display_label.configure(
                            text_color="red", text="Kiểm tra lại các ô điền đúng và không để trống")
                isSave = True

        return isSave
    
    def get_cabinet_by_id(self, cabinetId):
        newData = {}
        try:
            fb_cabinets = firebaseDB.child("Cabinet").child(cabinetId).get()
            newData.update(fb_cabinets.val())
        except IndexError:
            print("Location doesn't exist")

        return newData
    
    def get_box_by_cabinetId(self, cabinetId):
        newData = {}
        try:
            fb_boxes = firebaseDB.child("Box").order_by_child("cabinetId").equal_to(cabinetId).get()
            
            for key, value in fb_boxes.val().items():
                newData.update({
                    key: {
                        'id': value['id'],
                        'nameBox': value['nameBox'],
                    }
                })
        except IndexError:
            print("Box doesn't exist")
        
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
    
    def get_infos(self):
        cabinetId = self.view.root.cabinetId.get()
        self.view.cabinetData = self.get_cabinet_by_id(cabinetId)

        self.view.cabinetName.set(self.view.root.cabinetName.get())
        self.view.totalBox.set(self.view.cabinetData['totalBox'])
        
        cabinetId = self.view.root.cabinetId.get()
        boxResults = self.get_box_by_cabinetId(cabinetId)

        # Set data inside table with box results
        self.set_box_data(boxResults)
        self.view.boxTable.data.update(boxResults)

    # def upload_to_firebase(self, totalBox):
    #     cabinetId = self.view.cabinetId
    #     isCabinetUpload = self.upload_cabinet(totalBox)
    #     isLogUpload = self.upload_cabinetLog(cabinetId)
    #     isBoxUpload = self.upload_box(cabinetId)
    #     if isCabinetUpload and isLogUpload and isBoxUpload:
    #         return True

    # def upload_cabinet(self, totalBox):
    #     isUpload = None
    #     try:
    #         data = self.view.databaseController.get_last_cabinet()
    #         for value in data.values():
    #             cabinetRef = firebaseDB.child("Cabinet")

    #             newData = {
    #                 value['id']: {
    #                     'id': value['id'],
    #                     'nameCabinet': value['nameCabinet'],
    #                     'addDate': value['addDate'],
    #                     'status': value['status'],
    #                     'totalBox': totalBox,
    #                     'masterCode': value['masterCode'],
    #                     'masterCodeStatus': value['masterCodeStatus'],
    #                     'businessId': value['businessId'],
    #                     'locationId': value['locationId'],
    #                 }
    #             }

    #             cabinetRef.update(newData)
    #             self.view.cabinetId = value['id']
    #             isUpload = True
    #     except Exception as e:
    #         isUpload = False
    #         print("An error has occurred: ", e)

    #     return isUpload

    # def upload_box(self, cabinetId):
    #     isUpload = None
    #     try:
    #         data = self.view.databaseController.get_box_by_cabinetId(cabinetId)
    #         for box in data.values():
    #             boxRef = firebaseDB.child("Box")

    #             newData = {
    #                 box['id']: {
    #                     'id': box['id'],
    #                     'nameBox': box['nameBox'],
    #                     'status': box['status'],
    #                     'cabinetId': box['cabinetId']
    #                 }
    #             }

    #             boxRef.update(newData)
    #             isUpload = True
    #     except Exception as e:
    #         isUpload = False
    #         print("An error has occurred: ", e)

    #     return isUpload
    
    # def upload_cabinetLog(self, cabinetId):
    #     isUpload = None
    #     try:
    #         data = self.view.databaseController.get_cabinetLog_by_cabinetId(cabinetId)
    #         for log in data.values():
    #             logRef = firebaseDB.child("CabinetLog")

    #             newData = {
    #                 log['id']: {
    #                     'id': log['id'],
    #                     'messageTitle': log['messageTitle'],
    #                     'messageBody': log['messageBody'],
    #                     'messageStatus': log['messageStatus'],
    #                     'createDate': log['createDate'],
    #                     'cabinetId': log['cabinetId']
    #                 }
    #             }

    #             logRef.update(newData)
    #             isUpload = True
    #     except Exception as e:
    #         isUpload = False
    #         print("An error has occurred: ", e)

    #     return isUpload


class EditCabinetController():
    def __init__(self, view):
        self.view = view

    def set_location_data(self):
        results = self.view.databaseController.get_location_data()
        self.view.locationData.update(results)

        for key, value in self.view.locationData.items():
            self.view.locationComboboxValues.append(value['locationName'])
        
        self.view.location_combobox.configure(values=self.view.locationComboboxValues)

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
        self.view.masterCode.set(self.view.cabinetData['masterCode'])
        self.view.businessId.set(self.view.cabinetData['businessId'])
        self.view.locationId.set(self.view.cabinetData['locationId'])

        if self.view.cabinetData['status'] == 0:
            self.view.statusComboboxVar.set('No')
        elif self.view.cabinetData['status'] == 1:
            self.view.statusComboboxVar.set('Yes')

        self.set_location_data()

        for key, value in self.view.locationData.items():
            if value['locationId'] == self.view.cabinetData['locationId']:
                self.view.cabinetLocation.set(value['locationName'])
        
        boxResults = self.view.databaseController.get_box_by_cabinetId(self.view.cabinetId.get())

        # Set data inside table with box results
        self.set_box_data(boxResults)
        self.view.boxData.update(boxResults)

    def update_cabinet_data(self):
        cabinetValue = {
            'nameCabinet': self.view.cabinetName.get(),
            'status': self.view.status.get(),
            'masterCode': self.view.masterCode.get(),
            'masterCodeStatus': self.view.cabinetData['masterCodeStatus'],
            'businessId': self.view.businessId.get(),
            'locationId': self.view.locationId.get(),
            'id': self.view.cabinetId.get()
        }
        
        isUpdate = self.view.databaseController.update_cabinet_to_db(cabinetValue)
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
        
        logTitle = "Cập nhật Cabinet"
        logBody = "" + self.view.cabinetName.get() + " được cập nhật vào ngày: " + currentTime
        isSave = self.view.databaseController.save_cabinetLog_to_db(logTitle, logBody, self.view.cabinetId.get())
        
        if isSave:
            isUpdate = True
        
        return isUpdate
        
    def reupload_cabinet(self):
        isUpload = None
        try:
            cabinetId = self.view.cabinetId.get()
            cabinetRef = firebaseDB.child("Cabinet/", cabinetId)
            
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

    def reupload_box(self):
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
                # print(box['id'])
                boxId = box['id']
                boxRef = firebaseDB.child("Box/", boxId)

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


# class AddBoxController():
#     def __init__(self, view):
#         self.view = view

#     def set_cabinetId(self):
#         self.view.cabinetData = self.view.databaseController.get_cabinet_by_name(
#             self.view.root.cabinetName.get())

#         self.view.cabinetId = self.view.cabinetData['id']

#     def check_entries(self, value):
#         isCheck = False
#         if (not value['nameBox'] or not value['solenoidGpio'] 
#             or not value['switchGpio']  or not value['loadcellDout'] 
#             or not value['loadcellSck'] or not value['loadcellRf']):
#             # print(value)
#             isCheck = False
#         else:
#             isCheck = True

#         return isCheck

#     def add_more_box(self, data):
#         isSaved = False
        
#         for key, value in data.items():
#             isCheck = self.check_entries(value)
#             if not isCheck:
#                 self.view.display_label.configure(
#                     text_color="red",
#                     text="Hãy kiểm tra lại các ô điền đúng"
#                 )
#                 break
#             else:
#                 # print("Save box data: ", value)
#                 isSaved = self.view.databaseController.save_box_to_db(value)
#                 if isSaved:
#                     self.view.display_label.configure(
#                         text_color="green",
#                         text="Hộp tủ được tạo thành công")

#         return isSaved

#     def upload_more_boxes(self, cabinetId, limit):
#         isUpload = False
#         try:
#             results = self.view.databaseController.get_last_box_insert_by_cabinetId(cabinetId, limit)

#             for data in results:
#                 boxRef = firebaseDB.child("Box")

#                 newData = {
#                     data['id']: {
#                         'id': data['id'],
#                         'nameBox': data['nameBox'],
#                         'status': data['status'],
#                         'cabinetId': data['cabinetId']
#                     }
#                 }
                
#                 print(newData)

#                 boxRef.update(newData)

#             isUpload = True
#         except Exception as e:
#             isUpload = False
#             print("An error has occurred: ", e)

#         return isUpload
    
#     def update_total_box(self, cabinetId):
#         isUpdate = None
#         try:
#             cabinetRef = firebaseDB.child("Cabinet/", cabinetId)
#             boxResult = self.view.databaseController.get_box_by_cabinetId(cabinetId)
#             totalBox = len(boxResult)
            
#             newData = {
#                 'totalBox': totalBox
#             }
            
#             cabinetRef.update(newData)
#             isUpdate = True
#         except Exception as e:
#             isUpdate = False
#             print("An error has occurred: ", e)
        
#         return isUpdate


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

    def save_cabinet_to_db(self):
        isSave = False
        conn = self.opendb(db_file_name)
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M")
        
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()
            
            # generate random 6 digits
            digits = [i for i in range(0, 10)]
            randomDigits = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                randomDigits += str(digits[index])

            id = firebaseDB.generate_key()
            nameCabinet = self.view.cabinetName.get()
            addDate = currentTime
            status = self.view.cabinetStatus.get()
            masterCode = randomDigits
            masterCodeStatus = 1
            businessId = self.view.businessId.get()
            locationId = self.view.locationId.get()

            if not nameCabinet or not status or not locationId:
                return self.view.display_label.configure(text="Cabinet entries can't be empty")
            else:
                self.view.cabinetId = id
                
                cabinet = (id, nameCabinet, addDate, 
                           status, masterCode, masterCodeStatus, 
                           businessId, locationId)
                
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

    def save_cabinetLog_to_db(self, title, body, cabinetId):
        isSave = False
        conn = self.opendb(db_file_name)
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M")
        
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            id = firebaseDB.generate_key()
            messageTitle = title
            messageBody = body
            messageStatus = 1
            createDate = currentTime
            cabinetId = cabinetId
            
            cabinetLog = (id, messageTitle, 
                          messageBody, messageStatus, 
                          createDate, cabinetId)
            
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
    
    def save_box_to_db(self, record):
        conn = self.opendb(db_file_name)
        try:
            conn = sqlite3.connect(db_file_name)
            cur = conn.cursor()

            id = firebaseDB.generate_key()
            nameBox = record['nameBox']
            status = 1
            solenoidGpio = record['solenoidGpio']
            switchGpio = record['switchGpio']
            loadcellDout = record['loadcellDout']
            loadcellSck = record['loadcellSck']
            loadcellRf = record['loadcellRf']
            cabinetId = self.view.cabinetId

            box = (id, nameBox, status,
                   solenoidGpio, switchGpio, loadcellDout, 
                   loadcellSck, loadcellRf, cabinetId)

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

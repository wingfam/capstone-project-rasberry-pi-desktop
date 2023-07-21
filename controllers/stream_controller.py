import sqlite3 as sqlite3

from controllers.config_controller import DatabaseController
from services.firebase_config import firebaseDB

class StreamController():
    def __init__(self, view):
        self.view = view
        self.databaseController = DatabaseController(self)
        
    def cabinet_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Listening to cabinet stream")
        elif stream['event'] == 'patch':
            print("Patch event")
            path = stream['path']
            cabinetId = path[1: len(path)]
            snapshot = firebaseDB.child("Cabinet").order_by_key().equal_to(cabinetId).get().val()
            for key, value in snapshot.items():
                self.databaseController.update_cabinet(value)
        
    def mastercode_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Listening to master code stream")
        elif stream['event'] == 'patch':
            print("Patch event")
            path = stream['path']
            mastercodeId = path[1: len(path)]
            snapshot = firebaseDB.child("MasterCode").order_by_key().equal_to(mastercodeId).get().val()
            for key, value in snapshot.items():
                self.databaseController.update_master_code(value)
        
    def box_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Listening to box stream")
        elif stream['event'] == 'patch':
            print("Patch event")
            path = stream['path']
            boxId = path[1: len(path)]
            snapshot = firebaseDB.child("Box").order_by_key().equal_to(boxId).get().val()
            for key, value in snapshot.items():
                self.databaseController.update_box(value)
    
    def set_cabinet_stream(self, cabinetId):
        firebaseDB.child('Cabinet').order_by_key().equal_to(cabinetId).stream(
                self.cabinet_stream_handler, stream_id='cabinet_stream')
        
    def set_mastercode_stream(self, cabinetId):
        firebaseDB.child('MasterCode').order_by_child('cabinetId').equal_to(cabinetId).stream(
                self.mastercode_stream_handler, stream_id='master_code_stream')
    
    def set_box_stream(self, cabinetId):
        firebaseDB.child('Box').order_by_child('cabinetId').equal_to(cabinetId).stream(
                self.box_stream_handler, stream_id='box_stream')
    
    def set_all_stream(self):
        print('set all stream')
        cabinets = self.view.databaseController.get_all_cabinet_id()
        for value in cabinets.values():
            if value['id']:
                self.set_cabinet_stream(value['id'])
                self.set_mastercode_stream(value['id'])
                self.set_box_stream(value['id'])
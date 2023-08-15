import sqlite3 as sqlite3
import time

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
                self.databaseController.update_cabinet_to_db(value)
       
    def box_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Listening to box stream")
        elif stream['event'] == 'patch':
            print("Patch event")
            path = stream['path']
            boxId = path[1: len(path)]
            snapshot = firebaseDB.child("Box").order_by_key().equal_to(boxId).get().val()
            for key, value in snapshot.items():
                self.databaseController.update_box_patch_event(value)
    
    def set_cabinet_stream(self, cabinetId):
        cabinetStream = firebaseDB.child('Cabinet').order_by_key().equal_to(cabinetId).stream(
                self.cabinet_stream_handler, stream_id='cabinet_stream')
        time.sleep(0.01)
        return cabinetStream
     
    def set_box_stream(self, cabinetId):
        boxStream = firebaseDB.child('Box').order_by_child('cabinetId').equal_to(cabinetId).stream(
                self.box_stream_handler, stream_id='box_stream')
        time.sleep(0.01)
        return boxStream
    
    def set_all_stream(self):
        print('set all stream')
        stream = {}
        cabinets = self.view.databaseController.get_all_cabinet_id()
        for key, value in cabinets.items():
            cabinetId = value['id']
            stream = {
                cabinetId : {
                    'cabinetStream': self.set_cabinet_stream(cabinetId),
                    'boxStream': self.set_box_stream(cabinetId)
                }
            }
            
            self.view.globalStreams.update(stream)
            
    def close_all_stream(self):
        streams = self.view.globalStreams
        for key, value in streams.items():
            value['cabinetStream'].close()
            value['masterCodeStream'].close()
            value['boxStream'].close()
        print("All stream has close")
    
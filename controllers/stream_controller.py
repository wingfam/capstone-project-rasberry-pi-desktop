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
        
    def mastercode_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Listening to master code stream")
        elif stream['event'] == 'patch':
            print("Patch event")
            path = stream['path']
            mastercodeId = path[1: len(path)]
            snapshot = firebaseDB.child("MasterCode").order_by_key().equal_to(mastercodeId).get().val()
            for key, value in snapshot.items():
                self.databaseController.update_master_code_patch_event(value)
        
    def box_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Listening to box stream")
        elif stream['event'] == 'patch':
            print("Patch event")
            path = stream['path']
            boxId = path[1: len(path)]
            snapshot = firebaseDB.child("Box").order_by_key().equal_to(boxId).get().val()
            for key, value in snapshot.items():
                self.databaseController.update_box_from_patch(value)
    
    def set_cabinet_stream(self, cabinetId):
        cabinetStream = firebaseDB.child('Cabinet').order_by_key().equal_to(cabinetId).stream(
                self.cabinet_stream_handler, stream_id='cabinet_stream')
        time.sleep(0.01)
        cabinetStream.make_session()
        return cabinetStream
        
    def set_mastercode_stream(self, cabinetId):
        mastercodeStream = firebaseDB.child('MasterCode').order_by_child(
            'cabinetId').equal_to(cabinetId).stream(self.mastercode_stream_handler, stream_id='master_code_stream')
        time.sleep(0.01)
        mastercodeStream.make_session()
        return mastercodeStream
    
    def set_box_stream(self, cabinetId):
        boxStream = firebaseDB.child('Box').order_by_child('cabinetId').equal_to(cabinetId).stream(
                self.box_stream_handler, stream_id='box_stream')
        time.sleep(0.01)
        boxStream.make_session()
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
                    'masterCodeStream': self.set_mastercode_stream(cabinetId),
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
            
            # cabinetStream = value['cabinetStream']
            # masterCodeStream= value['masterCodeStream']
            # boxStreamT = value['boxStream']
            
            # if cabinetStream is None:
            #     print("Cabinet stream is None")
            #     pass
            # else:
            #     print("Cabinet stream is not None")
            #     print(cabinetStream)
            #     cabinetStream.close()
            
        print("All stream has close")
    
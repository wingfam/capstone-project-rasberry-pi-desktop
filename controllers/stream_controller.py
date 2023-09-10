import sqlite3 as sqlite3
import time

from controllers.config_controller import DatabaseController
from services.firebase_config import firebaseDB

class StreamController():
    def __init__(self, view):
        self.view = view
    
    def cabinet_stream_handler(self, stream):
        try:
            if stream['event'] == 'put':
                print("Cabinet stream Put event happened")
            elif stream['event'] == 'patch':
                print("Cabinet stream Patch event happened")
                path = stream['path']
                cabinetId = path[1: len(path)]
                snapshot = firebaseDB.child("Cabinet").order_by_key().equal_to(cabinetId).get().val()
                
                for value in snapshot.values():
                    self.view.databaseController.update_cabinet_to_db(value)
                    
        except Exception as e:
            print("An error has occurred: ", e)
            pass
       
    def box_stream_handler(self, stream):
        try:
            if stream['event'] == 'put':
                print("Box stream Put event happened")
            elif stream['event'] == 'patch':
                print("Box stream Patch event happened")
                path = stream['path']
                boxId = path[1: len(path)]
                snapshot = firebaseDB.child("Box").order_by_key().equal_to(boxId).get().val()
                
                for value in snapshot.values():
                    self.view.databaseController.update_box_patch_event(value)
                    
        except Exception as e:
            print("An error has occurred: ", e)
            pass
    
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
        cabinets = self.view.databaseController.get_cabinetId_cabinetName()
        for value in cabinets.values():
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
        for value in streams.values():
            value['cabinetStream'].close()
            value['boxStream'].close()
        print("All stream has close")
    
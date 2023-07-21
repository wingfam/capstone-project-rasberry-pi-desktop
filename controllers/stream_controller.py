import sqlite3 as sqlite3

from urllib.request import pathname2url
from constants.db_table import DbTable, db_file_name
from models.models import Cabinet, Box, MasterCode
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory
from constants.db_table import db_file_name

class StreamController():
    def __init__(self, view):
        self.view = view
        
    '''TODO: Hanlde data when put event happen'''
    def cabinet_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Put event")
        elif stream['event'] == 'patch':
            print("Patch event")
        print(stream["path"]) 
        print(stream["data"])
        print("\n")
    
    def set_cabinet_stream(self):
        cabinetId = None
        cabinets = self.view.databaseController.get_all_cabinet_id()
        for value in cabinets.values():
            cabinetId = value['id']
            firebaseDB.child('Cabinet/', cabinetId).stream(
                self.cabinet_stream_handler, stream_id='cabinet_stream')
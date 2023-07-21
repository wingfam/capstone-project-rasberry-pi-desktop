import sqlite3 as sqlite3

from urllib.request import pathname2url
from constants.db_table import DbTable, db_file_name
from controllers.config_controller import DatabaseController
from models.models import Cabinet, Box, MasterCode
from services.firebase_config import firebaseDB
from services.sqlite3 import dict_factory
from constants.db_table import db_file_name

class StreamController():
    def __init__(self, view):
        self.view = view
        self.databaseController = DatabaseController(self)
        
    '''TODO: Hanlde data when put event happen'''
    def cabinet_stream_handler(self, stream):
        if stream['event'] == 'put':
            print("Put event")
            print(stream['path'])
            print(stream['data'])
        elif stream['event'] == 'patch':
            print("Patch event")
            path = stream['path']
            # data = stream['data']
            Id = path[1: len(path)]
            snapshot = firebaseDB.child("Cabinet").order_by_key().equal_to(Id).get().val()
            for key, value in snapshot.items():
                self.databaseController.update_cabinet(value)
    
    def set_all_stream(self):
        cabinetId = None
        cabinets = self.view.databaseController.get_all_cabinet_id()
        for value in cabinets.values():
            cabinetId = value['id']
            # firebaseDB.child('Cabinet/', cabinetId).stream(
            #     self.cabinet_stream_handler, stream_id='cabinet_stream')
            firebaseDB.child('Cabinet').order_by_key().equal_to(cabinetId).stream(
                self.cabinet_stream_handler, stream_id='cabinet_stream')
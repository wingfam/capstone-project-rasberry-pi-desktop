db_file_name = r'smart_locker.db'

class DbTable():
    locationTable = '''
            CREATE TABLE IF NOT EXISTS Location (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                [nameLocation] TEXT,
                [address] TEXT,
                [status] INTEGER
            );
        '''
        
    cabinetTable = '''
        CREATE TABLE IF NOT EXISTS Cabinet (
            [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            [nameCabinet] TEXT,
            [addDate] TEXT,
            [isAvailable] INTEGER,
            [locationId] INTEGER NOT NULL,
            FOREIGN KEY (locationId)
                REFERENCES Location (id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
        );
    '''
    
    masterCodeTable = '''
        CREATE TABLE IF NOT EXISTS MasterCode (
            [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            [code] TEXT,
            [isAvailable] INTEGER,
            [cabinetId] INTEGER NOT NULL,
            FOREIGN KEY (cabinetId)
                REFERENCES Cabinet (id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
        );
    '''
    
    boxTable = '''
        CREATE TABLE IF NOT EXISTS Box (
            [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            [nameBox] TEXT,
            [size] TEXT,
            [width] INTEGER,
            [height] INTEGER,
            [isStore] INTEGER,
            [isAvailable] INTEGER,
            [solenoidGpio] INTEGER,
            [switchGpio] INTEGER,
            [loadcellDout] INTEGER,
            [loadcellSck] INTEGER,
            [cabinetId] INTEGER NOT NULL,
            FOREIGN KEY (cabinetId)
                REFERENCES Cabinet (id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
        );
    '''
    
    tableList = [locationTable, cabinetTable, masterCodeTable, boxTable]
db_file_name = r'smart_locker.db'

class DbTable():
    cabinetTable = '''
        CREATE TABLE IF NOT EXISTS Cabinet (
            [id] TEXT PRIMARY KEY NOT NULL,
            [name] TEXT,
            [addDate] TEXT,
            [isAvailable] INTEGER,
            [locationId] TEXT NOT NULL
        );
    '''
    
    masterCodeTable = '''
        CREATE TABLE IF NOT EXISTS MasterCode (
            [id] TEXT PRIMARY KEY NOT NULL,
            [code] TEXT,
            [isAvailable] INTEGER,
            [cabinetId] TEXT NOT NULL,
            FOREIGN KEY (cabinetId)
                REFERENCES Cabinet (id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
        );
    '''
    
    boxTable = '''
        CREATE TABLE IF NOT EXISTS Box (
            [id] TEXT PRIMARY KEY NOT NULL,
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
            [cabinetId] TEXT NOT NULL,
            FOREIGN KEY (cabinetId)
                REFERENCES Cabinet (id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
        );
    '''
    
    tableList = [cabinetTable, masterCodeTable, boxTable]
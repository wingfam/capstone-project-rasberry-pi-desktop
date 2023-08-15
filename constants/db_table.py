db_file_name = r'smart_locker.db'

class DbTable():
    cabinetTable = '''
        CREATE TABLE IF NOT EXISTS Cabinet (
            [id] TEXT PRIMARY KEY NOT NULL,
            [nameCabinet] TEXT,
            [addDate] TEXT,
            [status] INTEGER,
            [masterCode] TEXT,
            [masterCodeStatus] INTEGER,
            [businessId] TEXT NOT NULL,
            [locationId] TEXT NOT NULL
        );
    '''
    
    cabinetLog = '''
        CREATE TABLE IF NOT EXISTS CabinetLog (
            [id] TEXT PRIMARY KEY NOT NULL,
            [messageTitle] TEXT,
            [messageBody] TEXT,
            [createDate] TEXT,
            [messageStatus] INTEGER,
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
            [status] INTEGER,
            [solenoidGpio] INTEGER,
            [switchGpio] INTEGER,
            [loadcellDout] INTEGER,
            [loadcellSck] INTEGER,
            [loadcellRf] INTEGER,
            [cabinetId] TEXT NOT NULL,
            FOREIGN KEY (cabinetId)
                REFERENCES Cabinet (id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
        );
    '''
    
    tableList = [cabinetTable, cabinetLog, boxTable]
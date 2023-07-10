from services.auth import firebase_login
from services.firebase_config import firebaseDB

class Box():
    def __init__(self, Id, cabinetId, nameBox, size, isStore, isAvailable):
        self.Id = Id
        self.cabinetId = cabinetId
        self.nameBox = nameBox
        self.size = size
        self.isStore = isStore
        self.isAvailable = isAvailable

    @property
    def Id(self):
        return self.Id

    @property
    def cabinetId(self):
        return self.cabinetId

    @property
    def nameBox(self):
        return self.nameBox

    @property
    def size(self):
        return self.size

    @property
    def isStore(self):
        return self.isStore

    @property
    def isAvailable(self):
        return self.isAvailable

    @Id.setter
    def Id(self, value):
        self.Id = value

    @cabinetId.setter
    def cabinetId(self, value):
        self.cabinetId = value

    @nameBox.setter
    def nameBox(self, value):
        self.nameBox = value

    @size.setter
    def size(self, value):
        self.size = value

    @isStore.setter
    def isStore(self, value):
        self.isStore = value

    @isAvailable.setter
    def isAvailable(self, value):
        self.isAvailable = value

    async def saveToFirebase(self):
        fb_login = firebase_login()
        fb_ref = firebaseDB.child("Box")
        
        #Generate new key 
        newKey = fb_ref.generate_key() 
        
        # Data to save in database
        data = {
            "id" : newKey,
            "cabinetId": self.cabinetId,
            "nameBox": self.nameBox,
            "size": self.size,
            "isStore": self.isStore,
            "isAvailable": self.isAvailable,
        }
        
        # Update data to firebase
        fb_ref.child(newKey).update(data)
class Cabinet():
    def __init__(
        self, 
        id,
        name,
        addDate,
        isAvailable,
        locationId,
    ):
        self.id = id
        self.name = name
        self.addDate = addDate
        self.isAvailable = isAvailable
        self.locationId = locationId
    
    @property
    def id(self):
        return self.id

    @property
    def name(self):
        return self.name

    @property
    def addDate(self):
        return self.addDate

    @property
    def isAvailable(self):
        return self.isAvailable

    @property
    def locationId(self):
        return self.locationId
    
    @id.setter
    def id(self, value):
        self.id = value

    @name.setter
    def name(self, value):
        self.name = value

    @addDate.setter
    def addDate(self, value):
        self.addDate = value

    @isAvailable.setter
    def isAvailable(self, value):
        self.isAvailable = value

    @locationId.setter
    def locationId(self, value):
        self.locationId = value

    def __str__(self):
        return f"{self.name}, {self.addDate}, {self.isAvailable}"

class MasterCode():
    def __init__(
        self, 
        id,
        code,
        isAvailable,
        cabinetId,
    ):
        self.id = id
        self.code = code
        self.isAvailable = isAvailable
        self.cabinetId = cabinetId
    
    @property
    def id(self):
        return self.id

    @property
    def code(self):
        return self.code

    @property
    def isAvailable(self):
        return self.isAvailable

    @property
    def cabinetId(self):
        return self.cabinetId

    @id.setter
    def id(self, value):
        self.id = value

    @code.setter
    def code(self, value):
        self.code = value

    @isAvailable.setter
    def isAvailable(self, value):
        self.isAvailable = value

    @cabinetId.setter
    def cabinetId(self, value):
        self.cabinetId = value
        
    def __str__(self):
        return f"{self.code}, {self.isAvailable}"
        
class Box():
    def __init__(
        self, 
        id,
        nameBox,
        size,
        width,
        height,
        isAvailable,
        solenoidGpio,
        switchGpio, 
        loadcellDout,
        loadcellSck,
        cabinetId,
    ):
        self.id = id
        self.nameBox = nameBox
        self.size = size
        self.width = width
        self.height = height
        self.isAvailable = isAvailable
        self.solenoidGpio = solenoidGpio
        self.switchGpio = switchGpio
        self.loadcellDout = loadcellDout
        self.loadcellSck = loadcellSck
        self.cabinetId = cabinetId

    @property
    def id(self):
        return self.id

    @property
    def nameBox(self):
        return self.nameBox

    @property
    def size(self):
        return self.size

    @property
    def width(self):
        return self.width

    @property
    def height(self):
        return self.height

    @property
    def isAvailable(self):
        return self.isAvailable

    @property
    def solenoidGpio(self):
        return self.solenoidGpio

    @property
    def switchGpio(self):
        return self.switchGpio
    
    @property
    def loadcellDout(self):
        return self.loadcellDout
    
    @property
    def loadcellSck(self):
        return self.loadcellSck
    
    @property
    def cabinetId(self):
        return self.cabinetId

    @switchGpio.setter
    def switchGpio(self, value):
        self.switchGpio = value

    @switchGpio.setter
    def switchGpio(self, value):
        self.switchGpio = value
        
    @loadcellDout.setter
    def loadcellDout(self, value):
        self.loadcellDout = value
        
    @loadcellSck.setter
    def loadcellSck(self, value):
        self.loadcellSck = value
    
    @cabinetId.setter
    def cabinetId(self, value):
        self.cabinetId = value
    
    def __str__(self):
        return f"{self.nameBox}, {self.size}, {self.isAvailable}"
class Cabinet():
    def __init__(
        self,
        id,
        nameCabinet,
        status,
        masterCode,
        masterCodeStatus,
        addDate,
        businessId,
        locationId,
    ):
        self.id = id
        self.nameCabinet = nameCabinet
        self.status = status
        self.masterCode = masterCode
        self.masterCodeStatus = masterCodeStatus
        self.addDate = addDate
        self.businessId = businessId
        self.locationId = locationId

    @property
    def id(self):
        return self.id

    @property
    def nameCabinet(self):
        return self.nameCabinet

    @property
    def status(self):
        return self.status

    @property
    def masterCode(self):
        return self.masterCode

    @property
    def masterCodeStatus(self):
        return self.masterCodeStatus

    @property
    def addDate(self):
        return self.addDate

    @property
    def businessId(self):
        return self.businessId

    @property
    def locationId(self):
        return self.locationId
    

class CabinetLog():
    def __init__(
        self,
        id,
        cabinetId,
        messageTitle,
        messageBody,
        messageStatus,
        createDate
    ):
        self.id = id
        self.cabinetId = cabinetId
        self.messageTitle = messageTitle
        self.messageBody = messageBody
        self.messageStatus = messageStatus
        self.createDate = createDate

    @property
    def id(self):
        return self.id

    @property
    def cabinetId(self):
        return self.cabinetId

    @property
    def messageTitle(self):
        return self.messageTitle

    @property
    def messageBody(self):
        return self.messageBody

    @property
    def messageStatus(self):
        return self.messageStatus

    @property
    def createDate(self):
        return self.createDate


class Box():
    def __init__(
        self,
        id,
        nameBox,
        status,
        solenoidGpio,
        switchGpio,
        loadcellDout,
        loadcellSck,
        loadcellRf,
        cabinetId,
    ):
        self.id = id
        self.nameBox = nameBox
        self.status = status,
        self.solenoidGpio = solenoidGpio
        self.switchGpio = switchGpio
        self.loadcellDout = loadcellDout
        self.loadcellSck = loadcellSck
        self.loadcellRf = loadcellRf
        self.cabinetId = cabinetId

    @property
    def id(self):
        return self.id

    @property
    def nameBox(self):
        return self.nameBox

    @property
    def status(self):
        return self.status

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


class Gpio():
    def __init__(self, solenoid, magSwitch, loadcell):
        self.solenoid = solenoid
        self.magSwitch = magSwitch
        self.loadcell = loadcell

    @property
    def solenoid(self):
        return self.pin

    @property
    def magSwitch(self):
        return self.magSwitch

    @property
    def loadcell(self):
        return self.loadcell
    
    @solenoid.setter
    def solenoid(self, value):
        self.solenoid = value
        
    @magSwitch.setter
    def magSwitch(self, value):
        self.magSwitch = value
        
    @loadcell.setter
    def loadcell(self, value):
        self.loadcell = value
        

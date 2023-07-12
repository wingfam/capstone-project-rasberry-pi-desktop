class Box():
    def __init__(self, solenoid, magSwitch, loadcell):
        self.solenoid = solenoid
        self.magSwitch = magSwitch
        self.loadcell = loadcell

        @property
        def solenoid(self):
            return self.solenoid

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
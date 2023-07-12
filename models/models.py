class Box():
    def __init__(self, solenoid, magSwitch,):
        self.solenoid = solenoid
        self.magSwitch = magSwitch

        @property
        def solenoid(self):
            return self.solenoid

        @property
        def magSwitch(self):
            return self.magSwitch

        @solenoid.setter
        def solenoid(self, value):
            self.solenoid = value

        @magSwitch.setter
        def magSwitch(self, value):
            self.magSwitch = value
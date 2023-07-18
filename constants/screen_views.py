from views.add_cabinet_screen import AddCabinetScreen
from views.config_screen import ConfigScreen
from views.control_screen import ControlScreen
from views.main_screen import MainScreen
from views.delivery_screen import DeliveryScreen
from views.pickup_screen import PickupScreen
from views.completion_screen import CompletionScreen
from views.instruction_screen import InstructionScreen
from views.pre_config_screen import PreConfigScreen

class ScreenView():
    frame_views = {
        "MainScreen": MainScreen,
        "DeliveryScreen": DeliveryScreen,
        "PickupScreen": PickupScreen,
        "InstructionScreen": InstructionScreen,
        "CompletionScreen": CompletionScreen,
        "PreConfigScreen": PreConfigScreen,
        "ConfigScreen": ConfigScreen,
        "CabinetInfoScreen": AddCabinetScreen,
        "ControlScreen": ControlScreen,
    }
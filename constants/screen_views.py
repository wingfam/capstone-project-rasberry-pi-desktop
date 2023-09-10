from views.add_box_screen import AddBoxScreen
from views.add_cabinet_screen import AddCabinetScreen
from views.choose_cabinet_screen import ChooseCabinetScreen
from views.completion_screen import CompletionScreen
from views.config_screen import ConfigScreen
from views.control_screen import ControlScreen
from views.delivery_screen import DeliveryScreen
from views.edit_cabinet_screen import EditCabinetScreen
from views.instruction_screen import InstructionScreen
from views.main_screen import MainScreen
from views.pickup_screen import PickupScreen
from views.pre_config_screen import PreConfigScreen


class ScreenView():
    frame_views = {
        "MainScreen": MainScreen,
        "DeliveryScreen": DeliveryScreen,
        "PickupScreen": PickupScreen,
        "InstructionScreen": InstructionScreen,
        "CompletionScreen": CompletionScreen,
        "PreConfigScreen": PreConfigScreen,
        "ChooseCabinetScreen": ChooseCabinetScreen,
        "AddCabinetScreen": AddCabinetScreen,
        "ConfigScreen": ConfigScreen,
        "EditCabinetScreen": EditCabinetScreen,
        "AddBoxScreen": AddBoxScreen,
        "ControlScreen": ControlScreen,
    }
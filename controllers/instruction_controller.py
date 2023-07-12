import time
from services.auth import firebase_login
from services.firebase_config import firebaseDB

switch_hold_time = 3.0

def update_firebase(self, task):
    isError = False
    error_text= ""
    try:
        fb_login = firebase_login()
        isCompleted = True
        if task == "delivery":
            # Update booking code status to False
            newBCodeStatus = False
            isStore = True
            newBookingStatus = "Storing"
            
            code_id = self.controller.app_data["bookingCodeId"]
            booking_id = self.controller.app_data["bookingId"]
            box_id = self.controller.app_data["boxId"]
            
            firebaseDB.child("BookingCode", code_id).update(
                {"status": newBCodeStatus}, fb_login["idToken"])
            
            firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newBookingStatus}, fb_login["idToken"])

            firebaseDB.child("Box", box_id).update(
                {"isStore": isStore}, fb_login["idToken"])
            
            print("Delivery completed!")
            return isCompleted
        elif task == "pickup":
             # Update booking order status to False
            isStore = False
            newBCodeStatus = "Done"
            
            booking_id = self.controller.app_data["residentId"]
            residentId = self.controller.app_data["bookingId"]
            
            firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newBCodeStatus, "residentId": residentId}, fb_login["idToken"])
            
            print("Pickup completed!")
            return isCompleted
    except Exception as e:
        isError = True
        error_text= e
        print(error_text)
    
    if isError:
        return self.error_label.configure(
            text=error_text,
            foreground="red",
        )

# This gets called whenever the ON button is pressed
def unlock_door(model):
    print("Box's door is unlocked")
    model['solenoid_pin'].off()
    print('Magnetic switch value: ', model["magSwitch_pin"].value)

# This gets called whenever the OFF button is pressed
def lock_door(model):
    print("Box's door is locked")
    model['solenoid_pin'].on()
    print('Magnetic switch value: ', model['magSwitch_pin'].value)

def confirm_task(model):
    # Unlock box's door. Add wait for release event to magnetic switch
    # and check its state after 3 seconds
    unlock_door(model)
    isReleased = model['magSwitch_pin'].wait_for_release(5.0)

    if not isReleased:
        print('Magnetic switch is released: ', isReleased)
        lock_door(model)
        return False
    else:
        # Add when held event to the switch. If the switch is held for
        # a hold_time seconds, activate lock_door function (check pin 
        # declare for hold_time)
        print("Add event to magnetic switch")
        model['magSwitch_pin'].wait_for_press()
        if model['magSwitch_pin'].is_pressed:
            lock_door(model)
            time.sleep(switch_hold_time)
            return True
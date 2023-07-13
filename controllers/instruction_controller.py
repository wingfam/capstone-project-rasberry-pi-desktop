import time
from services.auth import firebase_login
from services.firebase_config import firebaseDB


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
            
            booking_id = self.controller.app_data["bookingId"]
            residentId = self.controller.app_data["residentId"]
            
            firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newBCodeStatus}, fb_login["idToken"])
            
            firebaseDB.child("BookingHistory").update(
                {"bookingId": booking_id, "residentId": residentId}, fb_login["idToken"])
            
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

def get_weight(model):
    loadcell = model['loadcell_pin']
    weightValue = max(0, int(loadcell.get_weight(5)))
    print("Check weight is done")
    return weightValue
    
def confirm_task(model, task):
    isConfirm = False
    waitTime = 5.0
    switchHoldTime = 1.0
    weightValue = 0
    
    # Unlock box's door. Add wait for release event to magnetic switch
    # and check its state after 5 seconds
    unlock_door(model)
    isReleased = model['magSwitch_pin'].wait_for_release(waitTime)

    if not isReleased:
        print('Magnetic switch is released: ', isReleased)
        lock_door(model)
    else:
        # Add when held event to the switch. If the switch is held for
        # a hold_time seconds, activate lock_door function (check pin 
        # declare for hold_time)
        print("Add event to magnetic switch")
        model['magSwitch_pin'].wait_for_press()
        if model['magSwitch_pin'].is_pressed:
            time.sleep(switchHoldTime)
            lock_door(model)
            weightValue = get_weight(model)
        
        # Check if loadcell detect any weight
        if weightValue != 0 and task == "delivery":
            isConfirm = True
        elif weightValue == 0 and task == "pickup":
            isConfirm = True
    
    return isConfirm
import time
from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB
from services.push_notification import PushNotificationService

def update_firebase(self, task):
    isError = False
    error_text= ""
    currentDateTime = datetime.now()
    currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        fb_login = firebase_login()
        isCompleted = False
        
        if task == "delivery":
            # Update booking code status to False
            newBookingStatus = False
            isStore = True
            newBookingStatus = "Storing"
            
            code_id = self.controller.app_data["bookingCodeId"]
            booking_id = self.controller.app_data["bookingId"]
            box_id = self.controller.app_data["boxId"]
            
            firebaseDB.child("BookingCode", code_id).update(
                {"status": newBookingStatus}, fb_login["idToken"])
            
            firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newBookingStatus}, fb_login["idToken"])

            firebaseDB.child("Box/", box_id).update(
                {"isStore": isStore}, fb_login["idToken"])
            
            residentId = self.controller.app_data["residentId"]
            nameBox = self.controller.app_data["nameBox"]
            
            messageTitle = "Giao hàng thàng công!"
            messageBody = "Bạn có một món hàng ở tủ số: " + nameBox + "Hãy vào trang Xem booking để lấy mã unlock"
            
            fb_notification = firebaseDB.child("Notification").order_by_child(
                "residentId").equal_to(residentId).get(fb_login["idToken"])
            
            send_notification(fb_notification, messageTitle, messageBody)
            
            save_notification(fb_login, fb_notification, messageTitle, messageBody)
            
            print("Delivery completed!")
            return isCompleted
        
        elif task == "pickup":
             # Update booking order status to False
            isStore = False
            isAvailable = True
            newBookingStatus = "Done"
            
            booking_id = self.controller.app_data["bookingId"]
            residentId = self.controller.app_data["residentId"]
            box_id = self.controller.app_data["boxId"]
            
            firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newBookingStatus}, fb_login["idToken"])
            
            firebaseDB.child("Box/", box_id).update(
                {"isAvailable": isAvailable, "isStore": isStore}, fb_login["idToken"])
            
            firebaseDB.child("BookingHistory").push(
                {"bookingId": booking_id, "residentId": residentId}, fb_login["idToken"])
            
            residentId = self.controller.app_data["residentId"]
            nameBox = self.controller.app_data["nameBox"]
            
            messageTitle = "Đã lấy hàng"
            messageBody = "Đơn hàng của bạn đã được lấy ra vào ngày: " + currentTime
            
            fb_notification = firebaseDB.child("Notification").order_by_child(
                "residentId").equal_to(residentId).get(fb_login["idToken"])
            
            send_notification(fb_notification, messageTitle, messageBody)
            
            save_notification(fb_login, fb_notification, messageTitle, messageBody)
            
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

def send_notification(fb_notification, messageTitle, messageBody):
    pushService = PushNotificationService()
    
    fb_item_list = list(fb_notification.val().items())
    
    fcm_token = fb_item_list[0][1].get("token")
    
    result = pushService.push_notification(fcm_token, messageTitle, messageBody)

    print(result)

def save_notification(fb_login, fb_notification, messageTitle, messageBody):
    currentDateTime = datetime.now()
    currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
    newKey = firebaseDB.generate_key()
    
    data = {
        "message/" + newKey: {
            "sendDate": currentTime,
            "message_title": messageTitle,
            "message_body": messageBody,
        }
    }
    
    fb_item_list = list(fb_notification.val().items())
    noti_id = fb_item_list[0][0]
    
    firebaseDB.child("Notification/", noti_id).update(data, fb_login["idToken"])
    
    print("Save notification successful")
    
# This gets called whenever the ON button is pressed
def unlock_door(model):
    print("Box's door is unlocked")
    model['solenoid_lock'].off()
    print('Magnetic switch value: ', model["magnetic_switch"].value)

# This gets called whenever the OFF button is pressed
def lock_door(model):
    print("Box's door is locked")
    model['solenoid_lock'].on()
    print('Magnetic switch value: ', model['magnetic_switch'].value)

# Get weight of the package and return its value
def get_weight(model):
    loadcell = model['loadcell']
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
    isReleased = model['magnetic_switch'].wait_for_release(waitTime)

    if not isReleased:
        print('Magnetic switch is released: ', isReleased)
        lock_door(model)
    else:
        # Add when held event to the switch. If the switch is held for
        # a hold_time seconds, activate lock_door function (check pin 
        # declare for hold_time)
        print("Add event to magnetic switch")
        model['magnetic_switch'].wait_for_press()
        if model['magnetic_switch'].is_pressed:
            time.sleep(switchHoldTime)
            lock_door(model)
            weightValue = get_weight(model)
        
        # Check if loadcell detect any weight
        if (weightValue != 0 and task == "delivery"):
            isConfirm = True
        elif task == "pickup"and weightValue == 0:
            isConfirm = True
    
    return isConfirm
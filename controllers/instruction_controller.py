import time
from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB
from services.push_notification import PushNotificationService

class InstructionController():
    def __init__(self, view):
        self.view = view

    def update_firebase(self, task):
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
                
                code_id = self.view.root.app_data["bookingCodeId"]
                booking_id = self.view.root.app_data["bookingId"]
                box_id = self.view.root.app_data["boxId"]
                
                firebaseDB.child("BookingCode", code_id).update(
                    {"status": newBookingStatus}, fb_login["idToken"])
                
                firebaseDB.child("BookingOrder", booking_id).update(
                    {"status": newBookingStatus}, fb_login["idToken"])

                firebaseDB.child("Box/", box_id).update(
                    {"isStore": isStore}, fb_login["idToken"])
                
                residentId = self.view.root.app_data["residentId"]
                nameBox = self.view.root.app_data["nameBox"]
                
                messageTitle = "Giao hàng thàng công!"
                messageBody = "Bạn có một món hàng ở tủ số: " + nameBox + "Hãy vào trang Xem booking để lấy mã unlock"
                
                fb_notification = firebaseDB.child("Notification").order_by_child(
                    "residentId").equal_to(residentId).get(fb_login["idToken"])
                
                self.send_notification(fb_notification, messageTitle, messageBody)
                
                self.save_notification(fb_login, fb_notification, messageTitle, messageBody)
                
                print("Delivery completed!")
                return isCompleted
            
            elif task == "pickup":
                # Update booking order status to False
                isStore = False
                status = True
                newBookingStatus = "Done"
                
                booking_id = self.view.root.app_data["bookingId"]
                residentId = self.view.root.app_data["residentId"]
                box_id = self.view.root.app_data["boxId"]
                
                firebaseDB.child("BookingOrder", booking_id).update(
                    {"status": newBookingStatus}, fb_login["idToken"])
                
                firebaseDB.child("Box/", box_id).update(
                    {"status": status, "isStore": isStore}, fb_login["idToken"])
                
                firebaseDB.child("BookingHistory").push(
                    {"bookingId": booking_id, "residentId": residentId}, fb_login["idToken"])
                
                residentId = self.view.root.app_data["residentId"]
                nameBox = self.view.root.app_data["nameBox"]
                
                messageTitle = "Đã lấy hàng"
                messageBody = "Đơn hàng của bạn đã được lấy ra vào ngày: " + currentTime
                
                fb_notification = firebaseDB.child("Notification").order_by_child(
                    "residentId").equal_to(residentId).get(fb_login["idToken"])
                
                self.send_notification(fb_notification, messageTitle, messageBody)
                
                self.save_notification(fb_login, fb_notification, messageTitle, messageBody)
                
                print("Pickup completed!")
                return isCompleted
        except Exception as e:
            print("An error has occurred: ", e)

    def send_notification(self, fb_notification, messageTitle, messageBody):
        pushService = PushNotificationService()
        
        fb_item_list = list(fb_notification.val().items())
        
        fcm_token = fb_item_list[0][1].get("token")
        
        result = pushService.push_notification(fcm_token, messageTitle, messageBody)

        print(result)

    def save_notification(self, fb_login, fb_notification, messageTitle, messageBody):
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
        newKey = firebaseDB.generate_key()
        
        data = {
            "message/" + newKey: {
                "sendDate": currentTime,
                "messageTitle": messageTitle,
                "messageBody": messageBody,
            }
        }
        
        fb_item_list = list(fb_notification.val().items())
        noti_id = fb_item_list[0][0]
        
        firebaseDB.child("Notification/", noti_id).update(data, fb_login["idToken"])
        
        print("Save notification successful")
        
    # This gets called whenever the ON button is pressed
    def unlock_door(self, model):
        model['solenoid'].off()

    # This gets called whenever the OFF button is pressed
    def lock_door(self, model):
        model['solenoid'].on()

    # Get weight of the package and return its value
    def get_weight(self, model):
        loadcell = model['loadcell']
        loadcell.power_up()
        time.sleep(0.01)
        
        weightValue = max(0, int(loadcell.get_weight(5)))

        time.sleep(0.01)
        loadcell.power_down()
        print("Check weight done!")
        
        return weightValue
        
    def confirm_task(self, model, task):
        isConfirm = False
        waitTime = 5.0
        switchHoldTime = 1.0
        weightValue = 0
        
        # Unlock box's door. Add wait for release event to magnetic switch
        # and check its state after 5 seconds
        self.unlock_door(model)
        isReleased = model['magSwitch'].wait_for_release(waitTime)

        if not isReleased:
            print('Magnetic switch is released: ', isReleased)
            self.lock_door(model)
        else:
            # Add when held event to the switch. If the switch is held for
            # a hold_time seconds, activate lock_door function (check pin 
            # declare for hold_time)
            print("Add event to magnetic switch")
            
            model['magSwitch'].wait_for_press()
            
            if model['magSwitch'].is_pressed:
                print("Magnetic switch is pressed")
                time.sleep(switchHoldTime)
                self.lock_door(model)
                weightValue = self.get_weight(model)
            
            # Check if loadcell detect any weight
            if (task == "delivery" and weightValue > 0):
                isConfirm = True
            elif (task == "pickup"and weightValue == 0):
                isConfirm = True
        
        return isConfirm
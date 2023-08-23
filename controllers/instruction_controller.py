import time
from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB
from services.push_notification import PushNotificationService

class InstructionController():
    def __init__(self, view):
        self.view = view
 
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
    
    def update_firebase(self, task):
        currentDateTime = datetime.now()
        currentTime = currentDateTime.strftime("%Y-%m-%d %H:%M")
        
        try:
            fb_login = firebase_login()
            isCompleted = False
            
            if task == "delivery":
                newBookingStatus = 3 # status "Storing"
                newBookingCodeStatus = 0 # status "Unavailable"
                newBoxStatus = 0 # status "Unavailable"
                
                bookingCodeId = self.view.root.app_data["bookingCodeId"]
                bookingId = self.view.root.app_data["bookingId"]
                boxId = self.view.root.app_data["boxId"]
                
                firebaseDB.child("BookingOrder", bookingId).update(
                    {"status": newBookingStatus}, fb_login["idToken"])

                firebaseDB.child("BookingCode", bookingCodeId).update(
                    {"status": newBookingCodeStatus}, fb_login["idToken"])
                
                firebaseDB.child("Box", boxId).update(
                    {"status": newBoxStatus}, fb_login["idToken"])
                
                customerId = self.view.root.app_data["customerId"]
                nameBox = self.view.root.app_data["nameBox"]
                
                notiTitle = "Gửi hàng thàng công!"
                notiBody = "Bạn có một món hàng ở tủ số: " + nameBox + ". Hãy vào trang Xem booking để lấy mã unlock"
                
                bookingLogTitle = "Gửi hàng"
                bookingLogBody = "Đơn hàng được gửi thành công ở tủ số "+ nameBox + " vào ngày " + currentTime
                
                self.add_booking_log(fb_login, bookingLogTitle, bookingLogBody, bookingId, currentTime)
                
                self.send_notification(fb_login, customerId, notiTitle, notiBody)
                
                self.save_notification(fb_login, customerId, notiTitle, notiBody, currentTime)
                
                isCompleted = True
                print("Delivery completed!")
            
            elif task == "pickup":
                newBookingStatus = 4 # status "Done"
                newBoxStatus = 1 # status "Available"
                
                bookingId = self.view.root.app_data["bookingId"]
                customerId = self.view.root.app_data["customerId"]
                boxId = self.view.root.app_data["boxId"]
                
                firebaseDB.child("BookingOrder", bookingId).update(
                    {"status": newBookingStatus}, fb_login["idToken"])
                
                firebaseDB.child("Box", boxId).update(
                    {"status": newBoxStatus}, fb_login["idToken"])
                
                customerId = self.view.root.app_data["customerId"]
                nameBox = self.view.root.app_data["nameBox"]
                
                notiTitle = "Lấy hàng thành công!"
                notiBody = "Đơn hàng của bạn được lấy ra vào ngày: " + currentTime
                
                bookingLogTitle = "Lấy hàng"
                bookingLogBody = "Đơn hàng được lấy ra ở tủ số "+ nameBox + " vào ngày " + currentTime
                
                self.add_booking_log(fb_login, bookingLogTitle, bookingLogBody, bookingId, currentTime)
                
                self.send_notification(fb_login, customerId, notiTitle, notiBody)
                
                self.save_notification(fb_login, customerId, notiTitle, notiBody, currentTime)
                
                isCompleted = True
                print("Pickup completed!")
            
        except Exception as e:
            print("An error has occurred: ", e)
        
        return isCompleted

    def add_booking_log(self, fb_login, logTitle, logBody, bookingId, currentTime):
        newKey = firebaseDB.generate_key()
        
        data = {
            "id": newKey,
            "bookingOrderId": bookingId,
            "messageTitle": logTitle,
            "messageBody": logBody,
            "messageStatus": 1,
            "createDate": currentTime,
        }
        
        firebaseDB.child("BookingOrderLog").push(data, fb_login["idToken"])
        
        print("Save notification successful")
    
    def send_notification(self, fb_login, customerId, messageTitle, messageBody):
        pushService = PushNotificationService()
        
        fb_notification = firebaseDB.child("Notification").order_by_child(
            "customerId").equal_to(customerId).get(fb_login["idToken"]).val()
        
        fcmToken = ""
        
        for key, value in fb_notification.items():
            print(value["token"])
            fcmToken = value["token"]
        
        result = pushService.push_notification(fcmToken, messageTitle, messageBody)

        print(result)

    def save_notification(self, fb_login, customerId, messageTitle, messageBody, currentTime):
        fb_notification = firebaseDB.child("Notification").order_by_child(
            "customerId").equal_to(customerId).get(fb_login["idToken"])
        
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
        
        firebaseDB.child("Notification", noti_id).update(data, fb_login["idToken"])
        
        print("Save notification successful")
       
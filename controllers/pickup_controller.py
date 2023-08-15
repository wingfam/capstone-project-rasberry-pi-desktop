from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

class PickupController():
    def __init__(self, view):
        self.view = view

    def check_unlock_code(self, input_data):
        isError = False
        error_text= ""
        if input_data.index("end") == 0:
            isError = True
            error_text = "Trường nhập không được để trống"
        else:
            try:
                # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
                fb_login = firebase_login()
                currentDate = datetime.now()
                inputCode = input_data.get()
                bookingId = ""
                
                fb_booking_order = firebaseDB.child("BookingOrder").order_by_child(
                    "unlockCode").equal_to(inputCode).get(fb_login["idToken"])
                
                for key, value in fb_booking_order.val().items():
                    status = value['status']
                    validDate = datetime.strptime(value['validDate'], "%Y-%m-%d %H:%M")
                    if status == 4 or currentDate > validDate:
                        isError = True
                        error_text = "Booking đã hết hạn"
                        break
                    else:
                        bookingId = value['id']
                        break
                
                return bookingId
            except IndexError:
                print("IndexError")
                isError = True
                error_text = "Mã unlock không đúng, vui lòng nhập lại"
        
        if isError:
            self.view.label_error.grid(
                padx=45,
                pady=116,
            )
            return self.view.label_error.configure(
                text=error_text,
                text_color="red",
            )
    
    def update_app_data(self, bookingId):
        fb_login = firebase_login()
        
        customerId = firebaseDB.child(
            "BookingOrder/", bookingId, "/customerId").get(fb_login["idToken"]).val()
        
        boxId = firebaseDB.child(
            "BookingOrder/", bookingId, "/boxId").get(fb_login["idToken"]).val()
        
        nameBox = firebaseDB.child(
            "Box/", boxId, "/nameBox").get(fb_login["idToken"]).val()
        
        self.view.root.app_data.update({
            "bookingId": bookingId,
            "customerId": customerId,
            "boxId": boxId,
            "nameBox": nameBox,
        })
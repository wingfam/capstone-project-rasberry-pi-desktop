from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseApp

class PickupController():
    def __init__(self, view):
        self.view = view

    def check_unlock_code(self, inputCode):
        isError = False
        error_text= ""
        bookingId = ""
        if not inputCode:
            error_text = "Trường nhập không được để trống"
            isError = True
        else:
            try:
                # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
                firebaseDB = firebaseApp.database()
                fb_login = firebase_login()
                
                fb_booking_order = firebaseDB.child("BookingOrder").order_by_child(
                    "unlockCode").equal_to(inputCode).get(fb_login["idToken"])
                
                for value in fb_booking_order.val().values():
                    status = value['status']
                    if status == 4 or status == 5:
                        error_text = "Booking không tồn tại"
                        isError = True
                    elif status == 2:
                        error_text = "Không thể mở khi chưa có hàng trong tủ"
                        isError = True
                    else:
                        bookingId = value['id']
                        return bookingId
                    
            except IndexError:
                error_text = "Mã unlock không đúng, vui lòng nhập lại"
                isError = True
        
        if isError:
            self.view.label_error.configure(text=error_text, foreground="red")
    
    def update_app_data(self, bookingId):
        firebaseDB = firebaseApp.database()
        fb_login = firebase_login()
        
        deviceId = firebaseDB.child(
            "BookingOrder/", bookingId, "/deviceId").get(fb_login["idToken"]).val()
        
        boxId = firebaseDB.child(
            "BookingOrder/", bookingId, "/boxId").get(fb_login["idToken"]).val()
        
        nameBox = firebaseDB.child(
            "Box/", boxId, "/nameBox").get(fb_login["idToken"]).val()
        
        self.view.root.app_data.update({
            "bookingId": bookingId,
            "deviceId": deviceId,
            "boxId": boxId,
            "nameBox": nameBox,
        })
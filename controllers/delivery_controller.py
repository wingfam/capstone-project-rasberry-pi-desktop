from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseApp

class DeliveryController():
    def __init__(self, view):
        self.view = view
    
    def check_booking_code(self, input_data):
        isError = False
        error_text= ""
        if input_data.index("end") == 0:
            error_text = "Trường nhập không được để trống"
            isError = True
        else:
            try:
                # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
                firebaseDB = firebaseApp.database()
                fb_login = firebase_login()
                currentDate = datetime.now()
                inputCode = input_data.get()
                order = ()
                
                fb_booking_code = firebaseDB.child("BookingCode").order_by_child(
                    "bcode").equal_to(inputCode).get(fb_login["idToken"])
                
                for value in fb_booking_code.val().values():
                    status = value['status']
                    validDate = datetime.strptime(value['validDate'], "%Y-%m-%d %H:%M")
                    if status == 0 or currentDate > validDate:
                        error_text = "Mã booking đã hết hạn, vui lòng tạo mã khác"
                        isError = True
                    else:
                        order = ({
                            'bookingCodeId': value['id'],
                            'bookingId': value['bookingId'],
                            'status': value['status']
                        })
                        return order
                        
            except IndexError:
                error_text = "Mã booking không đúng, vui lòng nhập lại"
                isError = True
        
        if isError:
            self.view.label_error.configure(text=error_text, foreground="red")

    def update_app_data(self, order):
        firebaseDB = firebaseApp.database()
        fb_login = firebase_login()
        
        deviceId = firebaseDB.child(
            "BookingOrder/", order['bookingId'], "/deviceId").get(fb_login["idToken"]).val()
        
        boxId = firebaseDB.child(
            "BookingOrder/", order['bookingId'], "/boxId").get(fb_login["idToken"]).val()
        
        nameBox = firebaseDB.child(
            "Box/", boxId, "/nameBox").get(fb_login["idToken"]).val()
        
        self.view.root.app_data.update({
            "bookingCodeId": order['bookingCodeId'],
            "bookingId": order['bookingId'],
            "deviceId": deviceId,
            "boxId": boxId,
            "nameBox": nameBox,
            "status": order['status'],
        })
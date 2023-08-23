from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

class DeliveryController():
    def __init__(self, view):
        self.view = view
    
    def check_booking_code(self, input_data):
        error_text= ""
        if input_data.index("end") == 0:
            error_text = "Trường nhập không được để trống"
            return self.view.label_error.configure(
                text=error_text,
                foreground="red")
        else:
            try:
                # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
                fb_login = firebase_login()
                currentDate = datetime.now()
                inputCode = input_data.get()
                order = ()
                
                fb_booking_code = firebaseDB.child("BookingCode").order_by_child(
                    "bcode").equal_to(inputCode).get(fb_login["idToken"])
                
                for key, value in fb_booking_code.val().items():
                    # print(value)
                    status = value['status']
                    validDate = datetime.strptime(value['validDate'], "%Y-%m-%d %H:%M")
                    if status == 0 or currentDate > validDate:
                        error_text = "Mã booking đã hết hạn, vui lòng tạo mã khác"
                        return self.view.label_error.configure(
                            text=error_text,
                            foreground="red")
                    else:
                        order = ({
                            'bookingCodeId': value['id'],
                            'bookingId': value['bookingId'],
                            'status': value['status']
                        })
                        break
                        
                return order
            except IndexError:
                error_text = "Mã booking không đúng, vui lòng nhập lại"
                return self.view.label_error.configure(
                    text=error_text,
                    foreground="red")

    def update_app_data(self, order):
        fb_login = firebase_login()
        
        customerId = firebaseDB.child(
            "BookingOrder/", order['bookingId'], "/customerId").get(fb_login["idToken"]).val()
        
        boxId = firebaseDB.child(
            "BookingOrder/", order['bookingId'], "/boxId").get(fb_login["idToken"]).val()
        
        nameBox = firebaseDB.child(
            "Box/", boxId, "/nameBox").get(fb_login["idToken"]).val()
        
        self.view.root.app_data.update({
            "bookingCodeId": order['bookingCodeId'],
            "bookingId": order['bookingId'],
            "customerId": customerId,
            "boxId": boxId,
            "nameBox": nameBox,
            "status": order['status'],
        })
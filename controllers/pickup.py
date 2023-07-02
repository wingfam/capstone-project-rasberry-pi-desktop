from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

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
            current_datetime = datetime.now()
            input_code = input_data.get()
            
            fb_unlock_code = firebaseDB.child("unlock_code").order_by_child(
                "ucode_name").equal_to(input_code).get(fb_login["idToken"])
            
            fb_item_list = list(fb_unlock_code.val().items())
            booking_id = fb_item_list[0][1].get("booking_id")
            
            valid_datetime = firebaseDB.child(
                "booking_order/", booking_id, "/booking_valid_datetime").get(fb_login["idToken"])
            
            valid_datetime = datetime.strptime(
                valid_datetime.val(), "%Y-%m-%d %H:%M:%S")
            
            booking_status = firebaseDB.child(
                "booking_order/", booking_id, "/booking_status").get(fb_login["idToken"]).val()
            
            if not booking_status or current_datetime > valid_datetime:
                isError = True
                error_text = "Booking Order đã hết hạn"
            else:
                item_list = []
                item_list.append(fb_login)
                item_list.append(fb_item_list)
                return item_list
        except IndexError:
            isError = True
            error_text = "Mã unlock không đúng, vui lòng nhập lại"
    
    if isError:
        self.label_error.grid(
            padx=45,
            pady=116,
        )
        return self.label_error.configure(
            text=error_text,
            text_color="red",
        )
        
def update_app_data(self, fb_item_list, fb_login):
    booking_id = fb_item_list[0][1].get("booking_id")
    locker_id = firebaseDB.child(
        "booking_order/", booking_id, "/locker_id").get(fb_login["idToken"]).val()
    locker_name = firebaseDB.child(
        "locker/", locker_id, "/locker_name").get(fb_login["idToken"]).val()
    
    self.controller.app_data.update({
        "BookingId": booking_id,
        "LockerId": locker_id,
        "LockerName": locker_name,
    })
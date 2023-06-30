from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

def verify_booking_code(self, input_data):
    # input_data = self.entry_code.get()
    current_datetime = datetime.now()
    try:
        # Login vào firebase mỗi lần gửi yêu cầu để tránh bị timeout
        isVerify = False;
        smart_locker = firebase_login()

        fb_booking_code = firebaseDB.child("booking_code").order_by_child(
            "bcode_name").equal_to(input_data).get(smart_locker["idToken"])
        items = list(fb_booking_code.val().items())
        valid_datetime = datetime.strptime(items[0][1].get(
            "bcode_valid_datetime"), "%Y-%m-%d %H:%M:%S")
        
        if current_datetime > valid_datetime:
            print("Mã booking đã hết hạn, vui lòng tạo booking khác.")
            return isVerify
        else:
            booking_id = items[0][1].get("booking_id")
            locker_id = firebaseDB.child(
                "booking_order/", booking_id, "/locker_id").get(smart_locker["idToken"]).val()
            locker_name = firebaseDB.child(
                "locker/", locker_id, "/locker_name").get(smart_locker["idToken"]).val()
            
            item_list = {
                "BookingId": booking_id,
                "LockerId": locker_id,
                "LockerName": locker_name
            }
            
            print(item_list["BookingId"])
    except IndexError:
        print("Mã booking không đúng, vui lòng nhập lại.")
        self.label.configure(
            text="Entry is empty",
            foreground="red",
        )
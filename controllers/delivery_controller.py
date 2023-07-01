from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

def check_booking_code(self, input_data):
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
            
            fb_booking_code = firebaseDB.child("booking_code").order_by_child(
                "bcode_name").equal_to(input_code).get(fb_login["idToken"])
            fb_item_list = list(fb_booking_code.val().items())
            valid_datetime = datetime.strptime(fb_item_list[0][1].get(
                "bcode_valid_datetime"), "%Y-%m-%d %H:%M:%S")
            
            if current_datetime > valid_datetime:
                isError = True
                error_text = "Mã booking đã hết hạn, vui lòng tạo booking khác"
            else:
                item_list = []
                item_list.append(fb_login)
                item_list.append(fb_item_list)
                return item_list
        except IndexError:
            isError = True
            error_text = "Mã booking không đúng, vui lòng nhập lại"
    
    if isError:
        self.label.grid(
            padx=45,
            pady=116,
        )
        return self.label.configure(
            text=error_text,
            foreground="red",
        )

def get_booking_info(fb_item_list, fb_login):
    booking_id = fb_item_list[0][1].get("booking_id")
    locker_id = firebaseDB.child(
        "booking_order/", booking_id, "/locker_id").get(fb_login["idToken"]).val()
    locker_name = firebaseDB.child(
        "locker/", locker_id, "/locker_name").get(fb_login["idToken"]).val()
    
    item_dict = {
        "BookingId": booking_id,
        "LockerId": locker_id,
        "LockerName": locker_name
    }
    
    print("LockerName: " + item_dict["LockerName"] + "\nBookingId: " + item_dict["BookingId"] + "\nLockerId: " + item_dict["LockerId"])
    
    return item_dict
         
def show_instructions(self, item_dict):
    booking_id = item_dict["BookingId"]
    print(booking_id)
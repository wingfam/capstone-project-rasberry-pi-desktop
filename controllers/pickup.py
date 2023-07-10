from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

async def check_unlock_code(self, input_data):
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
            input_code = input_data.get()
            
            fb_unlock_code = await firebaseDB.child("UnlockCode").order_by_child(
                "ucode").equal_to(input_code).get(fb_login["idToken"])
            
            fb_item_list = list(fb_unlock_code.val().items())
            bookingId = fb_item_list[0][1].get("bookingId")
            
            validDate = await firebaseDB.child(
                "BookingOrder/", bookingId, "/validDate").get(fb_login["idToken"])
            
            validDate = datetime.strptime(
                validDate.val(), "%Y-%m-%d %H:%M:%S")
            
            status = await firebaseDB.child(
                "BookingOrder/", bookingId, "/status").get(fb_login["idToken"]).val()
            
            if status == "Done" or currentDate > validDate:
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
#TODO:
'''Thêm lấy residentId để lưu vào BookingHistory'''
async def update_app_data(self, fb_item_list, fb_login):
    bookingId = fb_item_list[0][1].get("bookingId")
    
    residentId = await firebaseDB.child(
        "BookingOrder/", bookingId, "/residentId").get(fb_login["idToken"]).val()
    
    boxId = await firebaseDB.child(
        "BookingOrder/", bookingId, "/boxId").get(fb_login["idToken"]).val()
    
    nameBox = await firebaseDB.child(
        "Box/", boxId, "/nameBox").get(fb_login["idToken"]).val()
    
    self.controller.app_data.update({
        "bookingId": bookingId,
        "residentId": residentId,
        "boxId": boxId,
        "nameBox": nameBox,
    })
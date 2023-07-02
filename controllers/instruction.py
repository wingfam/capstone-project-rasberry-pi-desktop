from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

def confirm_task(self, data, task):
    isError = False
    error_text= ""
    try:
        fb_login = firebase_login()
        
        if task == "delivery":
            # Update booking code status to False
            isCompleted = True
            id = data["BookingCodeId"]
            newStatus = False
            firebaseDB.child("/booking_code/", id).update(
                {"Status": newStatus}, fb_login["idToken"])
            return isCompleted
        elif task == "pickup":
            booking_id = data["BookingId"]
            new_booking_status = False
            firebaseDB.child("/booking_order/", booking_id).update(
                {"booking_status": new_booking_status}, fb_login["idToken"])
            print("Pickup completed!")
    except Exception as e:
        isError = True
        error_text= e
        print(error_text)
    
    if isError:
        return self.error_label.configure(
            text=error_text,
            foreground="red",
        )
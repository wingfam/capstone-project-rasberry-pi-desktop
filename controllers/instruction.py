from datetime import datetime
from services.auth import firebase_login
from services.firebase_config import firebaseDB

def confirm_task(self, task):
    isError = False
    error_text= ""
    try:
        fb_login = firebase_login()
        
        if task == "delivery":
            # Update booking code status to False
            isCompleted = True
            newStatus = False
            code_id = self.controller.app_data["BookingCodeId"]
            
            firebaseDB.child("BookingCode", code_id).update(
                {"status": newStatus}, fb_login["idToken"])
            
            print("Delivery completed!")
            return isCompleted
        elif task == "pickup":
             # Update booking order status to False
            isCompleted = True
            newStatus = False
            booking_id = self.controller.app_data["BookingId"]
            
            firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newStatus}, fb_login["idToken"])
            
            print("Pickup completed!")
            return isCompleted
    except Exception as e:
        isError = True
        error_text= e
        print(error_text)
    
    if isError:
        return self.error_label.configure(
            text=error_text,
            foreground="red",
        )
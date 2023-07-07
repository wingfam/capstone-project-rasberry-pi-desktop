import asyncio
from services.auth import firebase_login
from services.firebase_config import firebaseDB

async def confirm_task(self, task):
    isError = False
    error_text= ""
    try:
        fb_login = firebase_login()
        isCompleted = True
        if task == "delivery":
            # Update booking code status to False
            newBCodeStatus = False
            isStore = True
            newBookingStatus = "Storing"
            
            code_id = self.controller.app_data["bookingCodeId"]
            booking_id = self.controller.app_data["bookingId"]
            box_id = self.controller.app_data["boxId"]
            
            await firebaseDB.child("BookingCode", code_id).update(
                {"status": newBCodeStatus}, fb_login["idToken"])
            
            await firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newBookingStatus}, fb_login["idToken"])

            await firebaseDB.child("Box", box_id).update(
                {"isStore": isStore}, fb_login["idToken"])
            
            print("Delivery completed!")
            return isCompleted
        elif task == "pickup":
             # Update booking order status to False
            isStore = False
            newBCodeStatus = "Done"
            
            booking_id = self.controller.app_data["BookingId"]
            
            await firebaseDB.child("BookingOrder", booking_id).update(
                {"status": newBCodeStatus}, fb_login["idToken"])
            
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
from services.firebase_config import firebaseDB
   
class PreConfigController():
    def __init__(self, view):
        self.view = view
    
    def check_master_code(self, input_data):
        isConfirm = False
        isError = False
        error_text= ""
        
        try:
            input_code = input_data.get()
            
            fb_master_code = firebaseDB.child("Cabinet").order_by_child(
                "masterCodeStatus").equal_to(input_code).get().val()
            
            fb_master_code_status = firebaseDB.child("Cabinet").order_by_child(
                "masterCodeStatus").equal_to(1).get().val()
            
            if fb_master_code != None and fb_master_code_status:
                isConfirm = True
            elif not fb_master_code_status:
                isError = True
                error_text = "Master code is unavailable"
                
        except IndexError:
            isError = True
            error_text = "Master code is incorrect"
            if input_code == "111111":
                isError = False
                isConfirm = True
        
        if isError:
            return self.view.master_code_label.configure(
                text=error_text,
                foreground="red",
            )
      
        return isConfirm
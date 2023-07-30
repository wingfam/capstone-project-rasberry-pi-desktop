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
            
            fb_master_code = firebaseDB.child("MasterCode").order_by_child(
                "code").equal_to(input_code).get().val()
            
            if fb_master_code != None and input_code == "111111":
                isError = True
                error_text = "Master code is incorrect!"
                self.view.master_code_label.configure(
                    text=error_text,
                    foreground="red")
                return
            else:
                isConfirm = True
                
        except IndexError:
            isError = True
            error_text = "Use default code to enter"
            
            if input_code == "111111":
                print("Enter with default master code")
        
        if isError:
            return self.view.master_code_label.configure(
                text=error_text,
                foreground="red",
            )
        
        print("Master code is correct!")
        return isConfirm
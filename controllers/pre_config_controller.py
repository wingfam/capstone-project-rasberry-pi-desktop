from services.firebase_config import firebaseDB
   
class PreConfigController():
    def __init__(self, view):
        self.view = view
    
    def check_master_code(self, input_data):
        isConfirm = False
        isError = False
        error_text= ""
        
        try:
            inputCode = input_data.get()
            
            fb_master_code = firebaseDB.child("Cabinet").order_by_child(
                "masterCode").equal_to(inputCode).get().val()
            
            for item in fb_master_code.items():
                # print(item[1])
                if (item[1]['masterCodeStatus'] == 1):
                    isConfirm = True
                else:
                    isError = True
                    error_text = "Mã master không thể dùng vào lúc này"
                
        except IndexError:
            isError = True
            error_text = "Mã master không đúng, vui lòng nhập lại"
        
        if isError:
            return self.view.error_label.configure(
                text=error_text,
                foreground="red",
            )
      
        return isConfirm
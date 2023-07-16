# Send to single device.
from pyfcm import FCMNotification

class PushNotificationService():    
    def __init__(self):
        # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
        apiKey = "AAAAeff4NC8:APA91bEstsmnsd_fqx04ZFPVzVn-8KMDXd9u4GONSR2Z1v28PpUyopLWtDTVaRYvte8sGkTBUyGGf8UYxcsuCaGxHwBDgd-lHttPBmh28lc64TJlyBFaX-km27dxX9doNU7bYfWV5OhY"
        self.push_service = FCMNotification(api_key=apiKey)
    
    def push_notification(self, registration_id, message_title, message_body):
        self.push_service.notify_single_device(
            registration_id=registration_id, 
            message_title=message_title, 
            message_body=message_body
        )
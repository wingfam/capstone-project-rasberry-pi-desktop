from services.firebase_config import firebaseApp, identity

def firebase_login():
    firebaseAuth = firebaseApp.auth()
    login = firebaseAuth.sign_in_with_email_and_password(identity['email'], identity['password'])
    return login
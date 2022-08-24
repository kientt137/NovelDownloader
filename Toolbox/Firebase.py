import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("truyenraw-64e91-firebase-adminsdk-9chfa-b94f0c803b.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://truyenraw-64e91-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference('/')
print(ref.child('1').get())

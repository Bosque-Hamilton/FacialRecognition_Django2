import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://studentattendance-fee90-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
data = {
    '321654':
        {
            "NAME": " Bosssssss",
            "COURSE": "COMPUTER SCIENCE",
            "STARTING_YEAR": 2019,
            'TOTAL_ATTENDANCE':6,
            'YEAR':4,
            "LAST_ATTENDANCE_TIME": '2022-12-11 00:54:34'
        },
    '852741':
        {
            "NAME": "EMILY BLUNT",
            "COURSE": "ECONOMICS",
            "STARTING_YEAR": 2018,
            'TOTAL_ATTENDANCE':6,
            'YEAR':5,
            "LAST_ATTENDANCE_TIME": '2022-12-11 00:54:34'
        },
    '963852':
        {
            "NAME": "ELON MASK",
            "COURSE": "PHYSICS",
            "STARTING_YEAR": 2020,
            'TOTAL_ATTENDANCE':6,
            'YEAR':2 ,
            "LAST_ATTENDANCE_TIME": '2022-12-11 00:54:34'
        }

}

for key, value in data.items():
    ref.child(key).set(value)
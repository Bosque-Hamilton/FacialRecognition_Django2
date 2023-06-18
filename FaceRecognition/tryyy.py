from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
import cv2
from django.views.decorators import gzip
from .models import StudentInfo
import pyrebase
from firebase_admin import db
import os
import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
# from firebase_admin import storage


config = {
    "apiKey": "AIzaSyCsS-0BqC9dHcnpx4je_zXOlNCb9MPzmu4",
    "authDomain": "studentattendance-fee90.firebaseapp.com",
    "databaseURL": "https://studentattendance-fee90-default-rtdb.firebaseio.com",
    "projectId": "studentattendance-fee90",
    "storageBucket": "studentattendance-fee90.appspot.com",
    "messagingSenderId": "938535852090",
    "appId": "1:938535852090:web:c3e3f3453fb718bd613d03",
    "measurementId": "G-7247BJ5Z63"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

file_path = 'AttendanceSystemWithFacialRecognition/FaceRecognition/EncodeFile.p'  # Replace with the actual file path

# Check if the file exists
if os.path.exists(file_path):
    # Open the file
    with open(file_path, 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)
    # Rest of your code...
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encoded file loaded")
else:
    print(f"Error: File '{file_path}' does not exist.")


# encodeListKnown, studentIds = encodeListKnownWithIds


def video_feed(request):
    def generate_frames():
        capture = cv2.VideoCapture(0)


        while True:
            ret, frame = capture.read()

            if not ret:
                break

            imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)


            if faceCurFrame:
                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                    matchesIndex = np.argmin(faceDis)

                    if matches[matchesIndex]:
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        bbox = 10 + x1, 10 + y1, x2 - x1, y2 - y1
                        img = cvzone.cornerRect(frame, bbox, rt=0)
                        id = studentIds[matchesIndex]

            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

@gzip.gzip_page
def index(request):

    student1 = StudentInfo()
    student1.name = "Kwame"
    student1.year = 400
    student1.img = 'elonmask.jpeg'


#
    student2 = StudentInfo()
    student2.name = "Kofi"
    student2.year = 200
    student2.img = 'billgates.jpeg'

    students =[student1, student2]



    return render(request, 'index.html', {'students': students})
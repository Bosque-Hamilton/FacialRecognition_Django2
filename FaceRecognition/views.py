from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
import cv2
from django.views.decorators import gzip
from .models import StudentInfo
import pyrebase
from firebase_admin import db

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



# Create your views here.

#
# def index(request):
#     @gzip.gzip_page
#     def webcam_feed(request):
#         # Set up the webcam
#         cap = cv2.VideoCapture(0)  # Use the appropriate webcam index (0 for default)
#
#         # Define a generator function to continuously read frames from the webcam
#         def generate_frames():
#             while True:
#                 # Read frame from the webcam
#                 ret, frame = cap.read()
#
#                 # Convert the frame to JPEG format
#                 ret, buffer = cv2.imencode('.jpg', frame)
#                 frame = buffer.tobytes()
#
#                 # Yield the frame as a chunked response
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
#         # Return the generator function as a StreamingHttpResponse
#         return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
#
#     return render(request,'index.html')



def video_feed(request):
    def generate_frames():
        capture = cv2.VideoCapture(0)

        while True:
            ret, frame = capture.read()

            if not ret:
                break

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
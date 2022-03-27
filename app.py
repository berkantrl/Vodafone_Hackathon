from flask import Flask, render_template, Response, request
import cv2
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore 

cred = credentials.Certificate("E:\web\Hackathon\photo.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

document = db.collection("data").document("test")

data = document.get().to_dict()


app=Flask(__name__)

camera = cv2.VideoCapture(0)

me_image = face_recognition.load_image_file("E:\web\Hackathon\Photos\\berkan.jpg")
face_encoding = face_recognition.face_encodings(me_image)[0]

ahmet_image = face_recognition.load_image_file("E:\web\Hackathon\Photos\\Ahmet.jpg")
ahmet_encoding = face_recognition.face_encodings(ahmet_image)[0]

yusuf_image = face_recognition.load_image_file("E:\web\Hackathon\Photos\\Yusuf.jpg")
yusuf_encoding = face_recognition.face_encodings(yusuf_image)[0]

guray_image = face_recognition.load_image_file("E:\web\Hackathon\Photos\\guray.jpg")
guray_encoding = face_recognition.face_encodings(guray_image)[0]


known_face_encodings = [
    face_encoding,
    ahmet_encoding,
    yusuf_encoding,
    guray_encoding
]

known_face_names = (
    "Berkan",
    "Ahmet",
    "Yusuf",
    "Güray"
)


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def control():
    success, frame = camera.read()  
    
            
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
    rgb_small_frame = small_frame[:, :, ::-1]
            
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    for face_encoding in face_encodings:
            
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
            
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        return name

def gen_frames():  
    while True:
        success, frame = camera.read()  
        if not success:
            break
        else:
            
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            rgb_small_frame = small_frame[:, :, ::-1]

            
           
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
               
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                

            
            

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/deneme', methods = ['GET', 'POST'])
def direct():
    name = control()
    if request.method == 'POST':
        if name in known_face_names :
            document.set({
                "veri" : name 
                })
            return render_template('numbers.html')
        else:
            return render_template('error.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)
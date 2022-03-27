from flask import Flask, render_template, Response, request
import firebase_admin
from firebase_admin import credentials, firestore 

app=Flask(__name__)

cred = credentials.Certificate("E:\web\Hackathon\photo.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

document = db.collection("data").document("test")

data = document.get().to_dict()

name = data["veri"]

document2 = db.collection("data").document("numbers")
data2 = document2.get().to_dict()
numbers_db = data2[name]
numbers = numbers_db.split(",")
number1 = numbers[0]
number2 = numbers[1]



@app.route('/numbers')
def index():
    return render_template("numbers.html")

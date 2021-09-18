from flask import Flask
from flask_cors import CORS, cross_origin
import cv2
import time
import mediapipe as mp
from math import sqrt

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

import cv2
import time
import mediapipe as mp
import numpy as np
from math import sqrt

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

HEIGHT = 480
WIDTH = 640

RIGHT_WRIST = mp_pose.PoseLandmark.RIGHT_WRIST
LEFT_WRIST = mp_pose.PoseLandmark.LEFT_WRIST
RIGHT_SHOULDER = mp_pose.PoseLandmark.RIGHT_SHOULDER
LEFT_SHOULDER = mp_pose.PoseLandmark.LEFT_SHOULDER
RIGHT_ELBOW = mp_pose.PoseLandmark.RIGHT_ELBOW
LEFT_ELBOW = mp_pose.PoseLandmark.LEFT_ELBOW
RIGHT_HIP = mp_pose.PoseLandmark.RIGHT_HIP
LEFT_HIP = mp_pose.PoseLandmark.LEFT_HIP
RIGHT_KNEE = mp_pose.PoseLandmark.RIGHT_KNEE
LEFT_KNEE = mp_pose.PoseLandmark.LEFT_KNEE
JOINTS = ((RIGHT_WRIST, 20),
          (LEFT_WRIST, 20),
          (RIGHT_SHOULDER, 1),
          (LEFT_SHOULDER, 1),
          (RIGHT_ELBOW, 8),
          (LEFT_ELBOW, 8),
          (RIGHT_HIP, 4),
          (LEFT_HIP, 4),
          (RIGHT_KNEE, 3),
          (LEFT_KNEE, 3))

VIDEO_NAME = 'Workout Dance'
VIDEO_PATH = 'videos/workout_vid.mp4'

MP_SETTINGS = {'min_detection_confidence': 0.5,
               'min_tracking_confidence': 0.5, 'model_complexity': 0}

def analyze_webcam(wc_frame, pose_wc):
    image = cv2.cvtColor(wc_frame, cv2.COLOR_BGR2RGB)
    try:
        results_wc = pose_wc.process(image)
    except Exception as e:
        pose_wc = mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw pose
    mp_drawing.draw_landmarks(image, results_wc.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(
                                    color=(245, 117, 66), thickness=2, circle_radius=4),
                                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    cv2.imshow('Raw Webcam Feed', image)

def analyze_pose(wc_frame, vid_frame, pose_wc, pose_vid, last_time, perf):
    # Webcam
    image = cv2.cvtColor(wc_frame, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (WIDTH, HEIGHT),
                        interpolation=cv2.INTER_AREA)
    try:
        results_wc = pose_wc.process(image)
    except Exception as e:
        pose_wc = mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Video footage
    image = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (WIDTH, HEIGHT),
                        interpolation=cv2.INTER_AREA)
    try:
        results_vid = pose_vid.process(image)
    except Exception as e:
        pose_vid = mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # FPS
    current_time = time.time()
    fps = 1/(current_time-last_time)
    last_time = current_time
    print(fps)

    # Perform calculations
    pl_wc = results_wc.pose_landmarks
    pl_vid = results_vid.pose_landmarks

    if pl_wc and pl_vid:
        pl_wc = pl_wc.landmark
        pl_vid = pl_vid.landmark
        for joint in JOINTS:
            if pl_wc[joint[0]] and pl_vid[joint[0]]:
                perf['dist'] += sqrt((pl_wc[joint[0]].x - pl_vid[joint[0]].x)**2 + (
                    pl_wc[joint[0]].y - pl_vid[joint[0]].y)**2) * joint[1]
                perf['weight'] += joint[1]


def calc_perf(perf):
    score = perf['dist']/perf['weight'] if perf['weight'] else 1
    perf['dist'] = 0
    perf['weight'] = 0
    print(score)
    if score >= 0.25:
        print('X')
    elif score >= 0.20:
        print('Good')
    elif score >= 0.15:
        print('Great')
    else:
        print('Excellent')
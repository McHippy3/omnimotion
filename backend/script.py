import cv2
import time
import mediapipe as mp
import numpy as np
from math import sqrt

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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

wc = cv2.VideoCapture(0)
vid = cv2.VideoCapture(VIDEO_PATH)

# Set dimensions of video
HEIGHT = 480
WIDTH = 640

wc.set(3, HEIGHT)
wc.set(4, WIDTH)

last_time = 0
last_perf_check = 0
perf = 0
perf_weight = 0

MP_SETTINGS = {'min_detection_confidence': 0.5,
               'min_tracking_confidence': 0.5, 'model_complexity': 0}

# Main loop
with mp_pose.Pose(**MP_SETTINGS) as pose_wc, \
        mp_pose.Pose(**MP_SETTINGS) as pose_vid:
    while wc.isOpened() and vid.isOpened():
        # Webcam
        wc_success, wc_frame = wc.read()
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

        # Video footage
        vid_success, vid_frame = vid.read()
        image = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (WIDTH, HEIGHT),
                           interpolation=cv2.INTER_AREA)
        try:
            results_vid = pose_vid.process(image)
        except Exception as e:
            pose_vid = mp_pose.Pose(
                min_detection_confidence=0.5, min_tracking_confidence=0.5)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw pose
        mp_drawing.draw_landmarks(image, results_vid.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(245, 117, 66), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # FPS
        current_time = time.time()
        fps = 1/(current_time-last_time)
        last_time = current_time
        # print(fps)

        # Perform calculations
        pl_wc = results_wc.pose_landmarks
        pl_vid = results_vid.pose_landmarks

        if pl_wc and pl_vid:
            pl_wc = pl_wc.landmark
            pl_vid = pl_vid.landmark
            for joint in JOINTS:
                if pl_wc[joint[0]] and pl_vid[joint[0]]:
                    perf += sqrt((pl_wc[joint[0]].x - pl_vid[joint[0]].x)**2 + (
                        pl_wc[joint[0]].y - pl_vid[joint[0]].y)**2) * joint[1]
                    perf_weight += joint[1]

        if current_time - last_perf_check > 1 and perf > 0:
            last_perf_check = current_time
            score = perf/perf_weight
            perf = 0
            perf_weight = 0
            print(score)
            if score >= 0.25:
                print('X')
            elif score >= 0.20:
                print('Good')
            elif score >= 0.15:
                print('Great')
            else:
                print('Excellent')

        cv2.imshow(VIDEO_NAME, image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    wc.release()
    vid.release()
    cv2.destroyAllWindows()

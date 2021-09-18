import cv2
import time
import mediapipe as mp
import numpy as np
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

VIDEO_NAME = 'Workout Dance'
VIDEO_PATH = 'videos/workout_vid.mp4'

wc = cv2.VideoCapture(0)
vid = cv2.VideoCapture(VIDEO_PATH)

# Set dimensions of video
HEIGHT = 480
WIDTH = 640

wc.set(3, HEIGHT)
wc.set(4, WIDTH)
vid.set(3, HEIGHT)
vid.set(4, WIDTH)

last_time = 0

# Main loop
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose_wc, \
     mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose_vid:
    while wc.isOpened() and vid.isOpened():
        # Framerate
        current_time = time.time()
        fps = 1/(current_time-last_time)
        last_time = current_time
        print(fps)

        # Webcam
        wc_success, wc_frame = wc.read()
        image = cv2.cvtColor(wc_frame, cv2.COLOR_BGR2RGB)
        try:
            results = pose_wc.process(image)
        except Exception as e:
            pose_wc= mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw pose
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        cv2.imshow('Raw Webcam Feed', image)

        # Video footage
        vid_success, vid_frame = vid.read()
        image = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
        try:
            results = pose_vid.process(image)
        except Exception as e:
            pose_vid = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw pose
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        cv2.imshow(VIDEO_NAME, image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    wc.release()
    vid.release()
    cv2.destroyAllWindows()

# OmniMotion
A full-stack application that allows you to "Just Dance" to anything. 

## Installation
1. `git clone https://github.com/McHippy3/omnimotion` in your preferred directory
2. Open the cloned folder in a code editor
3. Open a terminal and `cd` into the `frontend` folder
4. Run `npm i` to install the required node modules
5. Run `npm start` to start the React component
6. Open another terminal and `cd` into the `backend` folder
7. Create and activate a [python virtual environment](https://docs.python.org/3/tutorial/venv.html)
8. Run `pip install -r requirements.txt` to install the backend dependencies
9. Run `python app.py` to start the backend server
10. Navigate to `localhost:3000` on your web browser to begin using the application

Note: The application is relatively resource-intensive due to its use of motion tracking and machine learning. 

## How It Works
Using Google's MediaPipe ML library, the application is able to track the movements of both the user (via their webcam) and an individual from an uploaded video. The software
then analyzes the movements to track the relative similarity between the user and the video, assigning a corresponding score based on the user's performance.
![motion capture](https://github.com/McHippy3/htn-2021/blob/master/motion_capture.png)

## See It In Action
https://drive.google.com/file/d/16MuGKOmOyrkf2nSaGpdEEz_kmgnZhoeq/view?usp=sharing
![screenshot from web application](https://github.com/McHippy3/htn-2021/blob/master/ui.png)

## Technologies Used
 - ReactJS
 - SocketIO
 - Flask
 - OpenCV
 - MediaPipe

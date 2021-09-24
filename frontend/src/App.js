import { useState, useRef } from 'react';
import useInterval from './useInterval';
import ReactPlayer from "react-player";
import Button from '@mui/material/Button';
import './App.css';

import Webcam from "react-webcam";
import captureVideoFrame from "capture-video-frame";
import socketIOClient from "socket.io-client";

const ENDPOINT = "http://127.0.0.1:5000";

function App() {
  const webcamRef = useRef(null);

  const [videoFilePath, setVideoFilePath] = useState(null);
  const [videoPlaying, setVideoPlaying] = useState(false);
  const [perfVal, setPerfVal] = useState(0);
  const videoPlayer = useRef(null);

  const socket = socketIOClient(ENDPOINT);

  useInterval(() => {
    if (videoPlaying) {
      try {
        const vid_frame = captureVideoFrame(videoPlayer.current.getInternalPlayer(), 'jpeg').dataUri;
        socket.emit('new_frame', vid_frame);
      } catch (err) {
      }
    }
    else {
      const wc_frame = webcamRef.current.getScreenshot();
      socket.emit('new_frame', wc_frame);
    }
  }, 67);

  // socket.on('performance', x => {
  //   setPerfVal(x)
  // });

  const handleVideoUpload = (event) => {
    setVideoFilePath(URL.createObjectURL(event.target.files[0]));
    setVideoPlaying(true);
  }

  return (
    <div className="App">
      <header className="box">

        <div style={{ flex: 0.2, alignItems: 'center' }}>
          {/*TODO: Add logo*/}

          <h1 style={{ color: '#F0F4EF' }}>
            OmniMotion
          </h1>
        </div>


        <div style={{ display: 'flex', flex: 0.8, flexDirection: 'row' }}>
          {/*COL 1*/}
          <div style={{ flex: 0.5 }}>
            <Webcam style={{ borderRadius: 10, boxShadow: "0px 0px 70px red" }} ref={webcamRef} />
          </div>


          {/*COL 2*/}
          <div style={{ display: 'flex', flexDirection: 'column', flex: 0.5, alignItems: 'center', justifyContent: 'space-evenly' }}>
            <div style={{ flex: 0.8, display: videoPlaying ? "": "none" }}>
              <ReactPlayer id="video-file" ref={videoPlayer} url={videoFilePath} playing={videoPlaying} controls={true} />
            </div>
            <Button variant="contained" className="uploadButton" style={{ backgroundColor: "#F26430", width: '30%', display: videoPlaying ? "none" : "" }} component="label">
              Upload File
              <input
                type="file"
                accept=".mp4"
                onChange={handleVideoUpload}
                hidden
              />
            </Button>

          </div>



        </div>

      </header>
    </div>
  );
}

export default App;

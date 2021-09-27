import { useState, useRef, useEffect } from 'react';
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
  const [wcFlex, setWCFlex] = useState(0.5);
  const [vidFlex, setVidFlex] = useState(0.5);
  const videoPlayer = useRef(null);

  const socket = socketIOClient(ENDPOINT);

  useEffect(() => {
    socket.on('performance', newPerfVal => {
      setPerfVal(newPerfVal);
    });
  }, []);

  useInterval(() => {
    if (videoPlaying) {
      try {
        const wc_frame = webcamRef.current.getScreenshot();
        const vid_frame = captureVideoFrame(videoPlayer.current.getInternalPlayer(), 'jpeg').dataUri;

        // Downscale video frame using offscreen canvas
        var canvas = document.createElement('canvas'),
        ctx = canvas.getContext('2d');

        canvas.width = 768;
        canvas.height = 480;

        ctx.drawImage(vid_frame, 0, 0, 768, );

        socket.emit('new_frame_wc', wc_frame);
        socket.emit('new_frame_vid', canvas.toDataURL('image/jpeg'));
      } catch (err) {
        console.log(err)
      }
    }
  }, 1000);

  const handleVideoUpload = (event) => {
    setVideoFilePath(URL.createObjectURL(event.target.files[0]));
    setVideoPlaying(true);
    setWCFlex(0.3);
    setVidFlex(0.7)
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
          <div style={{ flex: wcFlex, alignItems: 'center'}}>
            <Webcam style={{ maxWidth: "80%", borderRadius: 10, boxShadow: "0px 0px 70px red" }} ref={webcamRef} />
          </div>


          {/*COL 2*/}
          <div style={{ display: 'flex', flexDirection: 'column', flex: vidFlex, alignItems: 'center', justifyContent: 'space-evenly' }}>
            <div style={{ display: videoPlaying ? '' : 'none' }}>
              <ReactPlayer id="video-file" width={1152} height={720} ref={videoPlayer} url={videoFilePath} playing={videoPlaying} controls={true} />
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

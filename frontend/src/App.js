import { useState, useRef, useEffect } from 'react';
import useInterval from './useInterval';
import ReactPlayer from "react-player";
import Button from '@mui/material/Button';
import './App.css';

import Webcam from "react-webcam";
import captureVideoFrame from "capture-video-frame";
import socketIOClient from "socket.io-client";
import resizedDataURL from './ImageHelpers';

import logo from './images/logo.jpg';

const ENDPOINT = "http://127.0.0.1:5000";

function App() {
  const webcamRef = useRef(null);

  const [videoFilePath, setVideoFilePath] = useState(null);
  const [videoPlaying, setVideoPlaying] = useState(false);
  const [performance, setPerformance] = useState("");
  const [shadowAnimation, setShadowAnimation] = useState("none")
  const [wcFlex, setWCFlex] = useState(0.5);
  const [vidFlex, setVidFlex] = useState(0.5);
  const videoPlayer = useRef(null);

  const socket = socketIOClient(ENDPOINT);

  useEffect(() => {
    socket.on('performance', newPerfVal => {
      switch (newPerfVal.value) {
        case 0:
          setShadowAnimation("fading-shadow-red");
          setPerformance("X")
          break;
        case 1:
          setShadowAnimation("fading-shadow-blue");
          setPerformance("Good")
          break;
        case 2:
          setShadowAnimation("fading-shadow-green");
          setPerformance("Great")
          break;
        case 3:
          setShadowAnimation("fading-shadow-yellow");
          setPerformance("Amazing!")
          break;
        default:
          setShadowAnimation("none");
          setPerformance("")
      }
    });
  }, [socket]);

  useInterval(async () => {
    if (videoPlaying) {
      try {
        const wc_frame = webcamRef.current.getScreenshot();
        const vid_frame = captureVideoFrame(videoPlayer.current.getInternalPlayer(), 'jpeg').dataUri;

        socket.emit('new_frame_wc', wc_frame);
        socket.emit('new_frame_vid', await resizedDataURL(vid_frame, 576, 360));
      } catch (err) {
        console.log(err)
      }
    }
  }, 250);

  const handleVideoUpload = (event) => {
    setVideoFilePath(URL.createObjectURL(event.target.files[0]));
    setVideoPlaying(true);
    setWCFlex(0.3);
    setVidFlex(0.7)
  }

  return (
    <div className="App">
      <header className="box">

        <div style={{ flex: 0.2, alignItems: 'center', padding: '10px' }}>
          <img src={logo} style={{ borderRadius: '10px' }} width="250px" alt="OmniMotion logo"/>
        </div>


        <div style={{ display: 'flex', flex: 0.8, flexDirection: 'row' }}>
          {/*COL 1*/}
          <div style={{ flex: wcFlex, alignItems: 'center' }}>
            <Webcam id="webcam" style={{ animation: `${shadowAnimation} 2s infinite` }} ref={webcamRef} />
            <h6 style={{ color: 'white' }}>{performance}</h6>
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

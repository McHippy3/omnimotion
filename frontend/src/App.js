import { useEffect, useRef } from 'react';
import logo from './logo.svg';
import Button from '@mui/material/Button';
import './App.css';

import Webcam from "react-webcam";
import socketIOClient from "socket.io-client";

const ENDPOINT = "http://127.0.0.1:5000";

function App() {
  const webcamRef = useRef(null);

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    setInterval(() => {
      const frame = webcamRef.current.getScreenshot();
      socket.emit("new_frame", frame);
    }, 67);
  }, []);

  return (
    <div className="App">
      <header className="box">

        <div style={{ flex: 0.2, alignItems: 'center'}}>
          {/*TODO: Add logo*/}

          <h1 style={{ color: '#F0F4EF' }}>
            OmniMotion
          </h1>
        </div>


        <div style={{display: 'flex', flex: 0.8, flexDirection: 'row'}}>
          {/*COL 1*/}
          <div style={{ flex: 0.5}}>

          </div>


          {/*COL 2*/}
          <div style={{display: 'flex', flex: 0.5, alignItems: 'center', justifyContent: 'center'}}>
          <Button variant="contained" className="uploadButton" style={{ backgroundColor: "#F26430", width: '30%'}} component="label">
                Upload File
                <input
                  type="file"
                  accept=".mp4"
                  hidden
                />
              </Button>
            
          </div>



        </div>

      </header>
      <Webcam ref={webcamRef} />
    </div>
  );
}

export default App;

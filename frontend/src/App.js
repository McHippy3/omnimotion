import { useEffect, useRef } from 'react';
import logo from './logo.svg';
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
        <img src={logo} className="App-logo" alt="logo" />
        <p style={{ color: '#F0F4EF' }}>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <Webcam ref={webcamRef} />
    </div>
  );
}

export default App;

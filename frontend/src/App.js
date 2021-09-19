import logo from './logo.svg';
import Button from '@mui/material/Button';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="box">
        <img src={logo} className="App-logo" alt="logo" />
        <p style={{ color: '#F0F4EF' }}>
          Edit <code>src/App.js</code> and save to reload.
        </p>

        <div style={{marginBottom: 15}}>
         <Button variant="contained" className = "uploadButton">
          Upload File
          </Button>
        </div>

        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

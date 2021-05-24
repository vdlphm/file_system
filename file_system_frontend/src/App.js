import logo from './logo.svg';
import './App.css';
import { Component } from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
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
    </div>
  );
}

const regexPath = new RegExp('^[/a-zA-Z0-9  _-]+$');
const regexName = new RegExp('^[a-zA-Z0-9  _-]+$');
// test path against regex
function matchPath(s) {
  return regexPath.test(s);
}
// test name against regex
function matchName(s) {
  return regexName.test(s);
}

export default App;

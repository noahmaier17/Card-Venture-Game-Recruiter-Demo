import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.js'; // Imports the main App component
import './index.css'; // Imports global styles

// Finds the HTML element with the ID 'root'
const rootElement = document.getElementById('root'); 

// Creates a React root
if (!rootElement) {
  throw new Error('Root element not found');
}
const root = ReactDOM.createRoot(rootElement);

// Renders the App component into the root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
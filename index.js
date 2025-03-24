import React from "react";
import ReactDOM from "react-dom/client";  // ✅ Use createRoot from React 18
import App from "./App";
import "./index.css";  // Make sure this file exists

const root = ReactDOM.createRoot(document.getElementById("root"));  
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

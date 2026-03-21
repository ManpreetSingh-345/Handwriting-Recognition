import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import axios from "axios";
import Cookies from "js-cookie";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true; // Ensures cookies are sent with cross-site requests

// If your server doesn't use the default cookie/header names, you can manually set the header:
const csrftoken = Cookies.get("csrftoken");
if (csrftoken) {
  axios.defaults.headers.common["X-CSRFToken"] = csrftoken; // Set common header for all request types
}

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);

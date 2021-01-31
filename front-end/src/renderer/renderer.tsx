/**
 * React renderer.
 */
// Import the styles here to process them with webpack
import "_public/style.css";

import * as React from "react";
import * as ReactDOM from "react-dom";

import App from "./App";
import { StateProvider } from "_utils/store";

ReactDOM.render(
  <StateProvider>
    <App />
  </StateProvider>,
  document.getElementById("app")
);

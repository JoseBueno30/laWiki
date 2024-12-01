import {RouterProvider } from "react-router-dom";

import router from "./router/router";
import { SettingsProvider } from "./context/settings-context";
import "./App.css";


function App() {
  return (
    <>
      <SettingsProvider>
        <RouterProvider router={router}/>
      </SettingsProvider>
    </>
  );
}

export default App;

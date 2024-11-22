import {RouterProvider } from "react-router-dom";

import router from "./layout/router";
import { ThemeProvider } from "./context/theme-context";
import "./App.css";


function App() {
  return (
    <>
      <ThemeProvider>
        <RouterProvider router={router}/>
      </ThemeProvider>
    </>
  );
}

export default App;

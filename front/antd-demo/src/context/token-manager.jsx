import { useEffect, createContext } from "react";
import { auth } from "../utils/firebase-config";

export const TokenContext = createContext();

export const TokenProvider = ({ children }) => {
  const token = localStorage.getItem("authToken");

  const checkAndUpdateToken = () => {
    console.log("AUTH LOGGED IN",auth.currentUser != null);
    if (token && auth.currentUser) {
      auth.currentUser.getIdToken(true).then((newToken) => {
        console.log("Token updated", newToken);
        localStorage.setItem("authToken", newToken);
      });
    }
  };

  useEffect(() => {
    // Check and update token the first time
    auth.onAuthStateChanged((user) => {
        if (user) {
          checkAndUpdateToken();
        }
      });

    console.log("Periodic token check started");
    const intervalID = setInterval(checkAndUpdateToken, 30 * 60 * 1000);
    return () => clearInterval(intervalID);
  }, []);

  return (
    <TokenContext.Provider value={{ token }}>{children}</TokenContext.Provider>
  );
};

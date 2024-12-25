import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import APIGateway from "../interceptor/interceptor";

const firebaseConfig = {
    apiKey: "AIzaSyCiEjTYN90jQ07q-4qtRjtB0i-bumpWtT0",
    authDomain: "lawiki-222c9.firebaseapp.com",
    projectId: "lawiki-222c9",
    storageBucket: "lawiki-222c9.firebasestorage.app",
    messagingSenderId: "10738864042",
    appId: "1:10738864042:web:52391fa0b6c08b2146e5d3"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const sendToBackend = async () => {
    try{
        const response = await APIGateway.get("http://localhost:3000/v2/users/me")
        return response;
    }catch(error){
        console.error("Error sending token to backend", error);
    }
}


export { auth, provider, signInWithPopup, sendToBackend};
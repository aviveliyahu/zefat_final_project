const { signInWithEmailAndPassword, createUserWithEmailAndPassword } = require("@firebase/auth");
const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

createUserWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // User account created successfully!
    const user = userCredential.user;
    console.log("New user created:", user);
    // ... Handle successful account creation (redirect, display success message)
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    console.error("Account creation error:", errorCode, errorMessage);
    // ... Handle account creation errors (display error message to user)
  });

signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // User signed in successfully!
    const user = userCredential.user;
    console.log("Logged in user:", user);
    // ... Handle successful sign-in (redirect, display success message)
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    console.error("Sign-in error:", errorCode, errorMessage);
    // ... Handle sign-in errors (display error message to user)
  });

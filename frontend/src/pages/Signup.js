// src/pages/Signup.js

import React from 'react';
import './Signup.css';

function Signup() {
    return (
        <div className="signup-container">
            <div className="signup-header">
                <h1>WELCOME!</h1>
                <h2>Create a New Account</h2>
            </div>
            <form className="signup-form">
                <input type="text" placeholder="Name" required />
                <input type="email" placeholder="Email" required />
                <input type="password" placeholder="Password" required />
                <button type="submit">CREATE ACCOUNT</button>
            </form>
            <p>Or</p>
            <button className="google-signup">Sign Up with Google</button>
            <p>Already have an account? <a href="/login">LOGIN</a></p>
        </div>
    );
}

export default Signup;

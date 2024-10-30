// src/pages/Login.js

import React from 'react';
import './Login.css';

function Login() {
    return (
        <div className="login-container">
            <div className="login-header">
                <h1>WELCOME BACK</h1>
                <h2>Log In to Your Account</h2>
            </div>
            <form className="login-form">
                <input type="email" placeholder="Email" required />
                <input type="password" placeholder="Password" required />
                <button type="submit">CONTINUE</button>
            </form>
            <p>Or</p>
            <button className="google-login">Log in with Google</button>
            <p>New User? <a href="/signup">SIGN UP HERE</a></p>
        </div>
    );
}

export default Login;

// src/pages/signup.js

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/signup.css';  // Adjusted path to locate signup.css
import { FaUser, FaLock, FaEnvelope } from 'react-icons/fa';

function Signup() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        handleSignup(email, name, password);
    };

    const handleSignup = (email, name, password) => {
        axios.post('/signup', { email, name, password })
            .then(response => {
                navigate('/login');
            })
            .catch(error => {
                setErrorMessage('Signup failed. Please try again.');
            });
    };

    return (
        <div className="signup-container">
            <div className="signup-card">
                <h2>Sign Up for Financial Literacy App</h2>
                <form onSubmit={handleSubmit}>
                    <div className="input-wrapper">
                        <label htmlFor="email"><FaEnvelope className="input-icon" /> Email:</label>
                        <input 
                            type="email" 
                            id="email"
                            placeholder="Enter your email" 
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-wrapper">
                        <label htmlFor="name"><FaUser className="input-icon" /> Name:</label>
                        <input 
                            type="text" 
                            id="name"
                            placeholder="Enter your name" 
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-wrapper">
                        <label htmlFor="password"><FaLock className="input-icon" /> Password:</label>
                        <input 
                            type="password"
                            id="password" 
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="signup-btn">Sign Up</button>
                </form>
                {errorMessage && <p className="error-message">{errorMessage}</p>}
                <div className="login-link">
                    <p>Already have an account? <Link to="/login">Login here</Link></p>
                </div>
            </div>
        </div>
    );
}

export default Signup;

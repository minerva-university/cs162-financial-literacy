import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaEnvelope, FaUser, FaLock, FaInfoCircle } from 'react-icons/fa';
import '../styles/signup.css';
import { register } from '../services/api';

function Signup() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [bio, setBio] = useState(''); // New state for bio
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await handleSignup(email, name, password, bio);
        } catch (error) {
            setErrorMessage('Signup failed. Please try again.');
        }
    };

    const handleSignup = async (email, name, password, bio) => {
        const data = await register(email, name, password, bio);
        if (data.success === "No") {
            setErrorMessage('Signup failed. Please try again.');
        } else {
            navigate('/login');
        }
    };

    return (
        <div className="signup-page">
            <div className="signup-card">
                <h2 className="signup-title">Create Your Account</h2>
                <p className="signup-subtitle">Join the Financial Literacy Platform</p>
                <form onSubmit={handleSubmit} className="signup-form">
                    <div className="form-group">
                        <label htmlFor="email">
                            <FaEnvelope className="input-icon" /> Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="name">
                            <FaUser className="input-icon" /> Name
                        </label>
                        <input
                            type="text"
                            id="name"
                            placeholder="Enter your name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">
                            <FaLock className="input-icon" /> Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            placeholder="Create a password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="bio">
                            <FaInfoCircle className="input-icon" /> Bio
                        </label>
                        <textarea
                            id="bio"
                            placeholder="Your time to Shine!"
                            value={bio}
                            onChange={(e) => setBio(e.target.value)}
                            rows="4"
                            required
                        />
                    </div>
                    <button type="submit" className="signup-button">
                        Sign Up
                    </button>
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                </form>
                <p className="signup-footer">
                    Already have an account? <Link to="/login">Login here</Link>
                </p>
            </div>
        </div>
    );
}

export default Signup;

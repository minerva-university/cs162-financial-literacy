import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaUser, FaLock } from 'react-icons/fa';
import { login } from '../services/api';  // Import the login function from your API services
import '../styles/login.css';  // Adjusted path to locate Login.css

function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    // Standard login with email and password
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const data = await login(email, password);
            if (data.success === "Yes") {
                // Store token if necessary, navigate to profile page
                navigate('/profile');
            } else {
                setErrorMessage('Invalid credentials or an error occurred. Please try again.');
            }
        } catch (error) {
            setErrorMessage('An error occurred during login. Please try again.');
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2>Login to Financial Literacy Platform</h2>
                <form onSubmit={handleSubmit}>
                    <div className="input-wrapper">
                        <label htmlFor="email"><FaUser className="input-icon" /> Email:</label>
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
                    <button type="submit" className="login-btn">Login</button>
                </form>
                {errorMessage && <p className="error-message">{errorMessage}</p>}
                <div className="register-link">
                    <p>Don't have an account? <Link to="/signup">Register here</Link></p>
                </div>
            </div>
        </div>
    );
}

export default Login;

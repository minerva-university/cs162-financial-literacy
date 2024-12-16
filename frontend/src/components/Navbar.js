import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { is_authenticated, logout } from '../services/api';
import "../styles/Navbar.css";

const Navbar = ({ onLogout }) => {
    const [authenticated, setAuthenticated] = useState(false);
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
            onLogout();
            navigate('/'); // Redirect to landing page
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    useEffect(() => {
        const checkAuthentication = async () => {
            const authStatus = await is_authenticated();
            setAuthenticated(authStatus);
        };
        checkAuthentication();
    }, []);

    return (
        <nav className="navbar-container">
            <div className="navbar-logo">
                <Link to="/" className="navbar-brand">Financial Literacy</Link>
            </div>
            <ul className="navbar-list">
                {authenticated ? (
                    <>
                        <li>
                            <Link to="/home" className="navbar-link">Home</Link>
                        </li>
                        <li>
                            <Link to="/profile" className="navbar-link">Profile</Link>
                        </li>
                        <li>
                            <button onClick={handleLogout} className="logout-button">Logout</button>
                        </li>
                    </>
                ) : (
                    <>
                        <li>
                            <Link to="/signup" className="navbar-link">Signup</Link>
                        </li>
                        <li>
                            <Link to="/login" className="navbar-link">Login</Link>
                        </li>
                    </>
                )}
            </ul>
        </nav>
    );
};

export default Navbar;

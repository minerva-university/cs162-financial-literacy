import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { is_authenticated, logout } from '../services/api';
import './Navbar.css';

const Navbar = () => {
    const [authenticated, setAuthenticated] = useState(false);

    const handleLogout = async () => {
        await logout();
        window.location.href = "/login";
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
                <Link to="/" className="navbar-brand">
                    Financial Literacy
                </Link>
            </div>
            <ul className="navbar-list">
                <li>
                    <Link to="/why-choose-us" className="navbar-link">
                        Why Choose Us
                    </Link>
                </li>
                {authenticated && (
                    <>
                        <li>
                            <Link to="/profile" className="navbar-link">
                                Profile
                            </Link>
                        </li>
                        <li>
                            <Link to="/" className="navbar-link">
                                Home
                            </Link>
                        </li>
                        <li>
                            <button
                                onClick={handleLogout}
                                className="logout-button"
                            >
                                Logout
                            </button>
                        </li>
                    </>
                )}
                {!authenticated && (
                    <>
                        <li>
                            <Link to="/signup" className="navbar-link">
                                Signup
                            </Link>
                        </li>
                        <li>
                            <Link to="/login" className="navbar-link">
                                Login
                            </Link>
                        </li>
                    </>
                )}
            </ul>
        </nav>
    );
};

export default Navbar;

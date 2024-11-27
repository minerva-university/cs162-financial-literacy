// src/components/Navbar.js

import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import { logout } from '../services/api';

const Navbar = () => {
    function handlelogout(){
        logout();
        Navigate("/login");
    }
    return (
        <nav>
            <Link to="/">Home</Link>
            <Link to="/signup">Signup</Link>
            <Link to="/login">Login</Link>
            <Link to="/profile">Profile</Link>
            <button onClick={handlelogout}>Logout</button>
        </nav>
    );
};

export default Navbar;

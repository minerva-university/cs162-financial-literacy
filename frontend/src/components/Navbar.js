// src/components/Navbar.js

import React from 'react';
import './Navbar.css';

function Navbar() {
    return (
        <nav className="navbar">
            <a href="/account">My Account</a>
            <a href="/settings">Settings</a>
        </nav>
    );
}

export default Navbar;

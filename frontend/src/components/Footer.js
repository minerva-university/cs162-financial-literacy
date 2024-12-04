import React from 'react';
import { Link } from 'react-router-dom';
import "../styles/Footer.css";


const Footer = () => {
    return (
        <footer className="footer-container">
            <div className="footer-content">
                <nav className="footer-links">
                    <Link to="/about" className="footer-link">About Us</Link>
                    <Link to="/contact" className="footer-link">Contact Us</Link>
                    <Link to="/faq" className="footer-link">FAQ</Link>
                </nav>
                <p className="footer-address">851 California St, San Francisco, CA</p>
            </div>
            <p className="footer-copyright">&copy; 2024 Financial Literacy Marketplace. All rights reserved.</p>
        </footer>
    );
};

export default Footer;

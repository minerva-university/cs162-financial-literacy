import React from 'react';
import { FaEnvelope, FaPhone, FaMapMarkerAlt } from 'react-icons/fa';
import '../styles/InfoPages.css';

const ContactUsPage = () => {
    return (
        <div className="info-page">
            <h1 className="info-page-title">Contact Us</h1>
            <p className="info-page-description">
                Have questions? We'd love to hear from you. Reach out to us through any of the
                channels below:
            </p>
            <div className="info-page-sections">
                <div className="info-page-card">
                    <FaEnvelope className="info-page-icon" />
                    <h2>Email Us</h2>
                    <p>support@financialliteracy.com</p>
                </div>
                <div className="info-page-card">
                    <FaPhone className="info-page-icon" />
                    <h2>Call Us</h2>
                    <p>+1 (123) 456-7890</p>
                </div>
                <div className="info-page-card">
                    <FaMapMarkerAlt className="info-page-icon" />
                    <h2>Visit Us</h2>
                    <p>851 California St, San Francisco, CA</p>
                </div>
            </div>
        </div>
    );
};

export default ContactUsPage;

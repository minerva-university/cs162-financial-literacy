import React from 'react';
import { FaEnvelope, FaPhone, FaMapMarkerAlt, FaFacebookF } from 'react-icons/fa';
import '../styles/ContactUs.css';

const ContactUsPage = () => {
    return (
        <div className="contact-page">
            <h1 className="contact-page-title">Contact Us</h1>
            <p className="contact-page-description">
                Have questions? We'd love to hear from you. Reach out to us through any of the
                channels below:
            </p>
            <div className="contact-page-sections">
                <div className="contact-page-card">
                    <FaEnvelope className="contact-page-icon" />
                    <h2 className="contact-card-title">Email Us</h2>
                    <p className="contact-card-content">support@financialliteracy.com</p>
                </div>
                <div className="contact-page-card">
                    <FaPhone className="contact-page-icon" />
                    <h2 className="contact-card-title">Call Us</h2>
                    <p className="contact-card-content">+1 (123) 456-7890</p>
                </div>
                <div className="contact-page-card">
                    <FaMapMarkerAlt className="contact-page-icon" />
                    <h2 className="contact-card-title">Visit Us</h2>
                    <p className="contact-card-content">851 California St, San Francisco, CA</p>
                </div>
                <div className="contact-page-card">
                    <FaFacebookF className="contact-page-icon" />
                    <h2 className="contact-card-title">Follow Us</h2>
                    <p className="contact-card-content">
                        Stay connected: <br />
                        <a href="https://facebook.com" className="social-link">Facebook</a>,{' '}
                        <a href="https://twitter.com" className="social-link">Twitter</a>,{' '}
                        <a href="https://instagram.com" className="social-link">Instagram</a>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ContactUsPage;

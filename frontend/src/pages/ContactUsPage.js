import React from 'react';
import { FaEnvelope, FaPhone, FaMapMarkerAlt, FaFacebookF } from 'react-icons/fa';
import '../styles/ContactUs.css';

const ContactUsPage = () => {
    return (
        <div className="contact-page">
            <div className="contact-hero">
                <h1 className="contact-page-title">Contact Us</h1>
                <p className="contact-page-description">
                    Have questions or suggestions? We’d love to hear from you. Connect with us through
                    any of the channels below and let’s build a financially confident community together.
                </p>
            </div>
            <div className="contact-page-sections">
                <div className="contact-page-card">
                    <FaEnvelope className="contact-page-icon" />
                    <h2 className="contact-card-title">Email Our Team</h2>
                    <div className="contact-card-content email-dropdown">
                        <label htmlFor="team-emails" className="email-label"><strong>Select a Team Member:</strong></label>
                        <select id="team-emails" className="email-select">
                            <option value="haneen@uni.minerva.edu">haneen@uni.minerva.edu</option>
                            <option value="jeevan@uni.minerva.edu">jeevan@uni.minerva.edu</option>
                            <option value="Daria@uni.minerva.edu">Daria@uni.minerva.edu</option>
                            <option value="Alaa@uni.minerva.edu">Alaa@uni.minerva.edu</option>
                            <option value="Jiyun@uni.minerva.edu">Jiyun@uni.minerva.edu</option>
                        </select>
                    </div>
                </div>
                <div className="contact-page-card">
                    <FaPhone className="contact-page-icon" />
                    <h2 className="contact-card-title">Call Us</h2>
                    <p className="contact-card-content">+1 (415) 623-9269</p>
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

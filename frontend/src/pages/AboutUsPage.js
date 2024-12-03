import React from 'react';
import { FaLightbulb, FaHandshake, FaChartLine } from 'react-icons/fa';
import '../styles/InfoPages.css';


const AboutUsPage = () => {
    return (
        <div className="info-page">
            <h1 className="info-page-title">About Us</h1>
            <p className="info-page-description">
                Welcome to the Financial Literacy Marketplace! Our mission is to empower individuals
                with the knowledge and tools they need to make informed financial decisions.
            </p>
            <div className="info-page-sections">
                <div className="info-page-card">
                    <FaLightbulb className="info-page-icon" />
                    <h2>Our Vision</h2>
                    <p>
                        To create a world where everyone has equal access to financial education
                        and opportunities.
                    </p>
                </div>
                <div className="info-page-card">
                    <FaHandshake className="info-page-icon" />
                    <h2>Our Mission</h2>
                    <p>
                        To connect mentors with mentees and provide resources to build financial
                        confidence and success.
                    </p>
                </div>
                <div className="info-page-card">
                    <FaChartLine className="info-page-icon" />
                    <h2>Our Impact</h2>
                    <p>
                        Over 10,000 users have gained access to mentorship and educational tools
                        through our platform.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AboutUsPage;

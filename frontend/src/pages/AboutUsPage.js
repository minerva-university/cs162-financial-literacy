import React from 'react';
import { FaLightbulb, FaHandshake, FaChartLine } from 'react-icons/fa';
import '../styles/AboutUsPage.css';

const AboutUsPage = () => {
    return (
        <div className="about-us-container">
            <div className="about-us-content">
                <div className="about-us-left">
                    <h1>About Us</h1>
                    <p>
                        Welcome to the Financial Literacy Marketplace! Our mission is to empower
                        individuals with the knowledge and tools they need to make informed financial
                        decisions.
                    </p>
                </div>
                <div className="about-us-divider"></div>
                <div className="about-us-right">
                    <div className="card-grid">
                        <div className="about-us-card">
                            <FaLightbulb className="about-us-icon" />
                            <h2>Our Vision</h2>
                            <p>
                                To create a world where everyone has equal access to financial
                                education and opportunities. We envision a community that thrives
                                on shared knowledge.
                            </p>
                        </div>
                        <div className="about-us-card">
                            <FaHandshake className="about-us-icon" />
                            <h2>Our Mission</h2>
                            <p>
                                To connect mentors with mentees and provide resources that enable
                                informed decision-making. Our goal is to foster financial empowerment
                                at every stage of your journey.
                            </p>
                        </div>
                        <div className="about-us-card-impact">
                            <FaChartLine className="about-us-icon" />
                            <h2>Our Impact</h2>
                            <p>
                                Over 10,000 users have gained access to mentorship and educational
                                tools through our platform. We continue to grow and innovate to serve
                                even more users worldwide.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AboutUsPage;

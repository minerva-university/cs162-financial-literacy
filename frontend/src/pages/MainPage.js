import React from 'react';
import { Link } from 'react-router-dom';
import './MainPage.css';

const MainPage = () => {
    return (
        <div className="mainpage-container">
            <header className="header-container">
                <h1 className="header-title">Welcome to the Financial Literacy Marketplace!</h1>
                <p className="header-subtitle">
                    Empowering you with tools, resources, and opportunities to thrive financially.
                </p>
            </header>
            <section className="resources-section">
                <div className="resources-grid">
                    <Link to="/mentors" className="resource-card mentors">
                        <div className="resource-icon">&#128101;</div>
                        <h3>Find Mentors</h3>
                        <div className="hover-tooltip">
                            Find personalized guidance from industry experts to help you grow and achieve your financial goals.
                        </div>
                    </Link>

                    <Link to="/feed" className="resource-card financial-posts">
                        <div className="resource-icon">&#128196;</div>
                        <h3>Financial Posts</h3>
                        <div className="hover-tooltip">
                            Access the latest insights, knowledge, and financial trends to sharpen your skills.
                        </div>
                    </Link>

                    <Link to="/scholarships" className="resource-card scholarships">
                        <div className="resource-icon">&#127891;</div>
                        <h3>Find Scholarships</h3>
                        <div className="hover-tooltip">
                            Secure funding opportunities and scholarships to achieve your dreams without financial barriers.
                        </div>
                    </Link>

                    <Link to="/internships" className="resource-card internships">
                        <div className="resource-icon">&#128188;</div>
                        <h3>Explore Internships</h3>
                        <div className="hover-tooltip">
                            Gain experience and grow your career prospects through impactful internships.
                        </div>
                    </Link>
                </div>
            </section>
        </div>
    );
};

export default MainPage;

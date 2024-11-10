// src/pages/MainPage.js

import React from 'react';
import './MainPage.css';

const MainPage = () => {
    return (
        <div className="mainpage-container">
            <header>
                <h1>Welcome to the Financial Literacy Marketplace!</h1>
                <p>Your one-stop shop for all financial resources!</p>
            </header>
            <div className="resources-grid">
                <div className="resource-card">Find Mentors</div>
                <div className="resource-card">Access Financial Resources</div>
                <div className="resource-card">Find Scholarships</div>
                <div className="resource-card">Explore our Internship Database</div>
            </div>
            <footer>
                <p>About Us | Contact Us | Learn More | 851 California St</p>
            </footer>
        </div>
    );
};

export default MainPage;

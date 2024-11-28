// src/pages/MainPage.js

import React from 'react';
import './MainPage.css';
import { Link } from 'react-router-dom';

const MainPage = () => {
    return (
        <div className="mainpage-container">
            <header>
                <h1 className=' font-serif text-3xl m-10'>Welcome to the Financial Literacy Marketplace!</h1>
                <p className=' font-serif text-xl'>Your one-stop shop for all financial resources!</p>
            </header>
            <div className="resources-grid p-10">
                
                <div className="resource-card">Find Mentors</div>
                <Link to="/feed" className=''>
                    <div className="resource-card bg-green-400">Financial Posts</div>
                </Link>
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

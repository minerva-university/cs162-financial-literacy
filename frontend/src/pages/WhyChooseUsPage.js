import React from 'react';
import './WhyChooseUsPage.css';

const WhyChooseUsPage = () => {
    return (
        <div className="why-choose-us-container">
            {/* Header Section */}
            <header className="why-header">
                <h1>Why Choose Us?</h1>
                <p>Discover the unique advantages of our platform.</p>
            </header>

            {/* Benefits Section */}
            <section className="benefits-section">
                <h2>Key Benefits</h2>
                <ul>
                    <li>Access curated resources and expert mentors.</li>
                    <li>Find scholarships and internships tailored to your needs.</li>
                    <li>Seamless navigation and a supportive community.</li>
                </ul>
            </section>

            {/* Reviews Section */}
            <section className="reviews-section">
                <h2>What People Say</h2>
                <div className="reviews-container">
                    {/* Review Card 1 */}
                    <div className="review-card">
                        <h3>John Doe</h3>
                        <p className="review-text">
                            "This platform helped me secure an internship at a top company! Highly recommended."
                        </p>
                        <div className="stars">
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                        </div>
                    </div>

                    {/* Review Card 2 */}
                    <div className="review-card">
                        <h3>Jane Smith</h3>
                        <p className="review-text">
                            "The resources and mentorship here are outstanding. It has been a game-changer for my career."
                        </p>
                        <div className="stars">
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                        </div>
                    </div>

                    {/* Review Card 3 */}
                    <div className="review-card">
                        <h3>Emily Johnson</h3>
                        <p className="review-text">
                            "I found amazing scholarships through this marketplace. A must-use for students!"
                        </p>
                        <div className="stars">
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                            <span>⭐</span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default WhyChooseUsPage;

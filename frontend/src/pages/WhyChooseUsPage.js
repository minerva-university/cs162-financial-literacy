import React from 'react';
import "../styles/WhyChooseUsPage.css";

const WhyChooseUsPage = () => {
    return (
        <div className="why-choose-us-container">
            {/* Hero Section */}
            <section className="hero-section">
                <h1>Why Choose Us?</h1>
                <p>Experience the ultimate platform for financial growth and career success.</p>
            </section>

            {/* Key Benefits Section */}
            <section className="benefits-section">
                <div className="benefits-container">
                    <div className="benefits-title">
                        <h2>Key Benefits</h2>
                        <p>Explore the unique features that set our platform apart from the rest.</p>
                    </div>
                    <div className="benefits-grid">
                        <div className="benefit-card">
                            <div className="benefit-icon">📘</div>
                            <h3>Curated Resources</h3>
                            <p>Gain access to expertly curated tools and resources to simplify your financial journey.</p>
                        </div>
                        <div className="benefit-card">
                            <div className="benefit-icon">🎓</div>
                            <h3>Scholarships & Internships</h3>
                            <p>Discover tailored opportunities to fund your education and launch your career.</p>
                        </div>
                        <div className="benefit-card">
                            <div className="benefit-icon">🌐</div>
                            <h3>Supportive Community</h3>
                            <p>Connect with mentors and peers who are passionate about your success.</p>
                        </div>
                        <div className="benefit-card">
                            <div className="benefit-icon">⚙️</div>
                            <h3>Seamless Navigation</h3>
                            <p>Enjoy a user-friendly interface that makes finding opportunities effortless.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Divider */}
            <div className="divider"></div>

            {/* Reviews Section */}
            <section className="reviews-section">
                <div className="reviews-header">
                    <h2>What People Say</h2>
                    <p>Hear from those who’ve experienced the benefits of our platform firsthand.</p>
                </div>
                <div className="reviews-grid">
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

import React from "react";
import { Link } from "react-router-dom";
import { FaEnvelope, FaPhone, FaMapMarkerAlt, FaFacebookF } from 'react-icons/fa';
import "../styles/LandingPage.css";

const LandingPage = () => {
    return (
        <div className="landing-container">
            {/* Hero Section */}
            <header className="landing-hero">
                <div className="landing-hero-content">
                    <h1 className="landing-title">Welcome to Financial Literacy Marketplace</h1>
                    <p className="landing-subtitle">
                        Your gateway to financial success through resources, mentorship, and growth opportunities.
                    </p>
                    <div className="landing-cta-buttons">
                        <Link to="/signup" className="landing-cta-button">Sign Up</Link>
                        <Link to="/login" className="landing-cta-button secondary">Login</Link>
                    </div>
                </div>
            </header>

            {/* About Section */}
            <section className="landing-about section-light">
                <h2>About Us</h2>
                <p>
                    We empower individuals with the tools, resources, and guidance they need to achieve financial
                    success. Explore our platform to discover how we can help you on your financial journey.
                </p>
            </section>

            {/* Key Benefits Section */}
            <section className="benefits-section section-dark">
                <div className="benefits-container">
                    <div className="benefits-title">
                        <h2>Why Choose Us?</h2>
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

            {/* Reviews Section */}
            <section className="reviews-section section-light">
                <div className="reviews-header">
                    <h2>What People Say</h2>
                    <p>Hear from those who’ve experienced the benefits of our platform firsthand.</p>
                </div>
                <div className="reviews-grid">
                    <div className="review-card">
                        <h3>Angela Jin</h3>
                        <p className="review-text">
                            "I appreciate how the app simplifies access to tailored financial resources and mentorship opportunities, making financial literacy approachable for all."
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
                        <h3>Rawan Khalifa</h3>
                        <p className="review-text">
                            "I love that the app encourages financial literacy knowledge sharing via credits and provides a supportive community."
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
                        <h3>Hilary Tang</h3>
                        <p className="review-text">
                            "I love the idea of a community that supports financial literacy. It’s been a fantastic experience."
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

            {/* Articles Section */}
            <section className="articles-section section-dark">
                <h2 className="articles-title">Explore Our Articles</h2>
                <p className="articles-subtitle">Learn more about financial literacy with our expert content.</p>
                <div className="articles-grid">
                    <div className="article-card">
                        <img src="/images/working-together.png" alt="Getting Started" className="article-image" />
                        <div className="article-content">
                            <h3>Getting Started</h3>
                            <p>Learn how to sign up, set up your profile, and explore our features effectively.</p>
                            <Link to="/article/1" className="read-more-link">Read More</Link>
                        </div>
                    </div>
                    <div className="article-card">
                        <img src="/images/getting-started.jpg" alt="Finding Resources" className="article-image" />
                        <div className="article-content">
                            <h3>Finding Resources</h3>
                            <p>Discover how to navigate mentorships, internships, and scholarships seamlessly.</p>
                            <Link to="/article/2" className="read-more-link">Read More</Link>
                        </div>
                    </div>
                    <div className="article-card">
                        <img src="/images/maximizing-benefits.png" alt="Maximizing Benefits" className="article-image" />
                        <div className="article-content">
                            <h3>Maximizing Benefits</h3>
                            <p>Tips on earning credits, accessing premium content, and staying informed.</p>
                            <Link to="/article/3" className="read-more-link">Read More</Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Contact Us Section */}
            <section className="contact-page section-light">
                <h2 className="contact-page-title">Contact Us</h2>
                <p className="contact-page-description">
                    Have questions? We'd love to hear from you. Reach out to us through any of the channels below:
                </p>
                <div className="contact-page-sections">
                    <div className="contact-page-card">
                        <FaEnvelope className="contact-page-icon" />
                        <h3 className="contact-card-title">Email Us</h3>
                        <p className="contact-card-content">support@financialliteracy.com</p>
                    </div>
                    <div className="contact-page-card">
                        <FaPhone className="contact-page-icon" />
                        <h3 className="contact-card-title">Call Us</h3>
                        <p className="contact-card-content">+1 (123) 456-7890</p>
                    </div>
                    <div className="contact-page-card">
                        <FaMapMarkerAlt className="contact-page-icon" />
                        <h3 className="contact-card-title">Visit Us</h3>
                        <p className="contact-card-content">851 California St, San Francisco, CA</p>
                    </div>
                    <div className="contact-page-card">
                        <FaFacebookF className="contact-page-icon" />
                        <h3 className="contact-card-title">Follow Us</h3>
                        <p className="contact-card-content">
                            Stay connected: <a href="https://facebook.com" className="social-link">Facebook</a>,{' '}
                            <a href="https://twitter.com" className="social-link">Twitter</a>,{' '}
                            <a href="https://instagram.com" className="social-link">Instagram</a>
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default LandingPage;

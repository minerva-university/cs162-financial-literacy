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
                    The Financial Literacy Marketplace was shaped by in-depth user interviews and iterative refinement.
                    We offer a robust credit system that encourages active participation, ensuring fair and
                    collaborative access to financial knowledge. By earning credits through activities like posting content 
                    or mentoring others, you unlock curated resources and schedule mentorship sessions that cost credits to access.
                    Our platform is designed for students and young professionals seeking reliable guidance, 
                    scholarships, internships, and meaningful mentorship connections. With transparent mentor profiles, 
                    clear credit mechanics, and intuitive navigation, we support your financial literacy journey
                    from start to finish.
                </p>
            </section>

            {/* Key Benefits Section */}
            <section className="benefits-section section-dark">
                <div className="benefits-container">
                    <div className="benefits-title">
                        <h2>Why Choose Us?</h2>
                        <p>Discover a platform built on user feedback, continuously refined to meet your needs.</p>
                    </div>
                    <div className="benefits-grid">
                        <div className="benefit-card">
                            <div className="benefit-icon">📘</div>
                            <h3>Curated Resources</h3>
                            <p>Access expertly selected tools and insights to guide your financial decisions.</p>
                        </div>
                        <div className="benefit-card">
                            <div className="benefit-icon">🎓</div>
                            <h3>Scholarships & Internships</h3>
                            <p>Find opportunities that match your goals, filtered by criteria like deadline or field.</p>
                        </div>
                        <div className="benefit-card">
                            <div className="benefit-icon">🌐</div>
                            <h3>Supportive Community</h3>
                            <p>Engage with peers and mentors who help you grow and leverage your credits wisely.</p>
                        </div>
                        <div className="benefit-card">
                            <div className="benefit-icon">⚙️</div>
                            <h3>Credit System</h3>
                            <p>Earn credits by posting and mentoring, spend them to access content or book sessions, ensuring a fair and dynamic environment.</p>
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
                        <img src="/images/Gabija.jpeg" alt="Gabija" className="review-image" />
                        <h3>Gabija Parnarauskaite</h3>
                        <p className="review-text">
                            "I appreciate how the app simplifies access to tailored financial resources and mentorship opportunities, making financial literacy approachable for all."
                        </p>
                        <div className="stars">
                            <span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span>
                        </div>
                    </div>
                    <div className="review-card">
                        <img src="/images/Fien.jpeg" alt="Fien" className="review-image" />
                        <h3>Fien Van Dan Hondel</h3>
                        <p className="review-text">
                            "I love that the app encourages financial literacy knowledge sharing via credits and provides a supportive community."
                        </p>
                        <div className="stars">
                            <span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span>
                        </div>
                    </div>
                    <div className="review-card">
                        <img src="/images/Dimitar.jpeg" alt="Dimitar" className="review-image" />
                        <h3>Dimitar Ivanov</h3>
                        <p className="review-text">
                            "I love the idea of a community that supports financial literacy. It’s been a fantastic experience."
                        </p>
                        <div className="stars">
                            <span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Team Section */}
            <section className="team-section section-dark">
                <div className="team-header">
                    <h2>Meet Our Team</h2>
                    <p>Our dedicated group of professionals is committed to your financial literacy journey.</p>
                </div>
                <div className="team-grid">
                    <div className="team-card">
                        <img src="/images/Jiyun.jpg" alt="Jiyun" className="team-image" />
                        <h3 className="team-name">Jiyun</h3>
                        <p className="team-bio">
                            Hi, I am a Computer Science & Sustainability student at Minerva University. I am a Quant trader and software engineer, interested in using advanced technology for enhancing sustainability.
                        </p>
                    </div>
                    <div className="team-card">
                        <img src="/images/Alaa.jpg" alt="Alaa" className="team-image" />
                        <h3 className="team-name">Alaa</h3>
                        <p className="team-bio">
                            Hi! I am Alaa, a computer science student. I aim to blend technology and finance, helping people manage their financial lives more efficiently.
                        </p>
                    </div>
                    <div className="team-card">
                        <img src="/images/Daria.jpg" alt="Daria" className="team-image" />
                        <h3 className="team-name">Daria</h3>
                        <p className="team-bio">
                            I am Daria, a computer science and data science student from Ukraine. I focus on creating meaningful projects that build community and reflect my identity.
                        </p>
                    </div>
                    <div className="team-card">
                        <img src="/images/Haneen.jpg" alt="Haneen" className="team-image" />
                        <h3 className="team-name">Haneen</h3>
                        <p className="team-bio">
                            I am Haneen, a Computer Science and Finance student passionate about blending technology with financial markets to forge smarter investment solutions.
                        </p>
                    </div>
                    <div className="team-card">
                        <img src="/images/Jeevan.jpg" alt="Jeevan" className="team-image" />
                        <h3 className="team-name">Jeevan</h3>
                        <p className="team-bio">
                        Hello, I’m a software engineering enthusiast passionate about building impactful tools with Python, JavaScript, and machine learning. Having worked across four countries, I thrive in collaborative environments.
                        </p>
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
                        <h3 className="contact-card-title">Email Our Team</h3>
                        <div className="contact-card-content email-dropdown">
                            <label htmlFor="team-emails" className="email-label"><strong>Select a Team Email:</strong></label>
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
                        <h3 className="contact-card-title">Call Us</h3>
                        <p className="contact-card-content">+1 (415) 623-9269</p>
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
                            Stay connected:&nbsp;
                            <a href="https://facebook.com" className="social-link">Facebook</a>,{' '}
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

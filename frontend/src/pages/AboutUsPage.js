import React from 'react';
import { FaLightbulb, FaHandshake, FaChartLine } from 'react-icons/fa';
import '../styles/AboutUsPage.css';

const AboutUsPage = () => {
    return (
        <div className="about-page-container">
            {/* Hero / Introduction Section */}
            <section className="about-hero">
                <h1>About Us</h1>
                <p className="hero-text">
                    Welcome to the Financial Literacy Marketplace! We are committed to empowering students 
                    and young professionals with the knowledge and tools needed to make informed financial decisions. 
                    Through curated resources, mentorship programs, and an engaging credit system, we strive 
                    to build a community where everyone can confidently navigate their financial journey.
                </p>
            </section>

            {/* Vision, Mission, Impact Section */}
            <section className="about-vmi-section">
                <div className="vmi-card">
                    <FaLightbulb className="vmi-icon" />
                    <h2>Our Vision</h2>
                    <p>
                        We envisage a world where accessible and transparent financial education is standard. 
                        By fostering a global community of learners and mentors, we aim to elevate financial literacy for everyone.
                    </p>
                </div>
                <div className="vmi-card">
                    <FaHandshake className="vmi-icon" />
                    <h2>Our Mission</h2>
                    <p>
                        We connect learners with mentors, providing the tools and guidance needed for 
                        informed financial decisions. Our platform empowers users at every stage of their journey.
                    </p>
                </div>
                <div className="vmi-card">
                    <FaChartLine className="vmi-icon" />
                    <h2>Our Impact</h2>
                    <p>
                        We have proudly onboarded our initial 10 users, marking the start of a growing community. 
                        Each new member expands our network of knowledge, collaboration, and sustainable financial empowerment.
                    </p>
                </div>
            </section>

            {/* Team Section */}
            <section className="about-team-section">
                <h2 className="team-title">Meet Our Team</h2>
                <p className="team-subtitle">A dedicated group of professionals, passionate about enhancing global financial literacy.</p>
                <div className="team-wrapper">
                    <div className="team-card">
                        <img src="/images/Alaa.jpg" alt="Alaa" className="team-image" />
                        <h3 className="team-name">Alaa</h3>
                        <p className="team-bio">
                        Hi! I am Alaa, a computer science student. I am an aspiring software engineer with an interest in finances and helping people manage their financial lives more efficiently.
                        </p>
                    </div>
                    <div className="team-card">
                        <img src="/images/Daria.jpg" alt="Daria" className="team-image" />
                        <h3 className="team-name">Daria</h3>
                        <p className="team-bio">
                        I am Daria, a computer science and data science student from Ukraine. I am interested in creating meaningful projects that reflect my identity and contribute to the community
                        </p>
                    </div>
                    <div className="team-card">
                        <img src="/images/Haneen.jpg" alt="Haneen" className="team-image" />
                        <h3 className="team-name">Haneen</h3>
                        <p className="team-bio">
                        I am Haneen, a CS & Finance student driven by a passion for blending technology with the dynamic world of financial markets –– eager to explore how emerging technologies can reshape investment strategies.
                        </p>
                    </div>
                    <div className="team-card">
                        <img src="/images/Jiyun.jpg" alt="Jiyun" className="team-image" />
                        <h3 className="team-name">Jiyun</h3>
                        <p className="team-bio">
                        Hi, I am Computer Science & Sustainability student at Minerva University. I am a Quant trader and software engineer, interested in the advanced technology for enhancing sustainability.
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
        </div>
    );
};

export default AboutUsPage;

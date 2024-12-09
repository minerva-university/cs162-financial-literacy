import React from 'react';
import { Link } from 'react-router-dom';
import "../styles/MainPage.css";


const MainPage = () => {
    const articles = [
        {
            title: "Getting Started",
            description: "Learn how to sign up, set up your profile, and explore our features effectively.",
            readTime: "5 min read",
            imgSrc: "/images/working-together.png",
            link: "/article/1"
        },
        {
            title: "Finding Resources",
            description: "Discover how to navigate mentorships, internships, and scholarships seamlessly.",
            readTime: "4 min read",
            imgSrc: "/images/getting-started.jpg",
            link: "/article/2"
        },
        {
            title: "Maximizing Benefits",
            description: "Tips on earning credits, accessing premium content, and staying financially informed.",
            readTime: "6 min read",
            imgSrc: "/images/maximizing-benefits.png",
            link: "/article/3"
        }
    ];

    return (
        <div className="mainpage-container">
            <header className="header-container">
                <h1 className="header-title">Welcome to the Financial Literacy Marketplace!</h1>
                <p className="header-subtitle">
                    Empowering you with tools, resources, and opportunities to thrive financially.
                </p>
            </header>

            {/* Resource Cards Section */}
            <section className="resources-section">
                <div className="resources-grid">
                    {/* Existing Resource Cards */}
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

            {/* Learn How to Use the Platform Section */}
            <section className="learn-platform-section">
                <div className="learn-header">
                    <h2>Learn How to Use Our Platform</h2>
                    <p>
                        Explore comprehensive guides, insightful articles, and helpful tips to make the most of the Financial Literacy Marketplace.
                    </p>
                </div>
                <div className="articles-grid">
                    {articles.map((article, index) => (
                        <Link to={article.link} className="article-card" key={index}>
                            <img
                                src={article.imgSrc}
                                alt={`Article ${index + 1}`}
                                className="article-image"
                            />
                            <h3>{article.title}</h3>
                            <p>{article.description}</p>
                            <span className="read-time">{article.readTime}</span>
                        </Link>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default MainPage;

import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/ArticlesPage.css';

const ArticlesPage = () => {
    const articles = [
        {
            id: 1,
            title: 'Understanding Budgeting Basics',
            description: 'Learn how to manage your finances effectively through simple budgeting techniques.',
            image: '/images/working-together.png',
            readTime: '3 min read',
        },
        {
            id: 2,
            title: 'How to Save for Your Goals',
            description: 'Explore strategies for saving money to achieve short-term and long-term goals.',
            image: '/images/getting-started.jpg',
            readTime: '3 min read',
        },
        {
            id: 3,
            title: 'Building Credit: A Step-by-Step Guide',
            description: 'Understand the importance of credit and how to improve your credit score over time.',
            image: '/images/maximizing-benefits.png',
            readTime: '1 min read',
        },
    ];

    return (
        <div className="articles-page">
            <h1 className="articles-title">Common Questions</h1>
            <p className="articles-subtitle">Explore our resources to enhance your financial knowledge.</p>
            <div className="articles-grid">
                {articles.map((article) => (
                    <div key={article.id} className="article-card">
                        <img src={article.image} alt={article.title} className="article-image" />
                        <div className="article-content">
                            <h3>{article.title}</h3>
                            <p>{article.description}</p>
                            <span className="read-time">{article.readTime}</span>
                            <Link to={`/article/${article.id}`} className="read-more-link">
                                Read More
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ArticlesPage;

import React from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ArticlePage.css';

const ArticlePage = () => {
    const { articleId } = useParams();

    const articleContent = {
        1: {
            title: 'Getting Started',
            image: '/images/working-together.png',
            content: (
                <>
                    <p>
                        Welcome to the Financial Literacy Marketplace! Here’s your quick guide to signing up and setting yourself up for success:
                    </p>
                    <ol>
                        <li>
                            <strong>Sign Up:</strong> Create your profile by entering your name, email, and setting up a secure password. Bonus points for picking a profile picture that screams confidence!
                        </li>
                        <li>
                            <strong>Explore Your Dashboard:</strong> Your personalized hub. From mentors to scholarships, it’s all just a click away.
                        </li>
                        <li>
                            <strong>Set Your Goals:</strong> Use the goal-setting tool to define your financial priorities. Want to save for a vacation? Pay off a loan? We’ve got you covered.
                        </li>
                        <li>
                            <strong>Navigate the Marketplace:</strong> Click, explore, and bookmark resources. It’s like shopping, but for your financial future.
                        </li>
                    </ol>
                    <p>
                        By the end of this guide, you’ll feel empowered to take charge of your financial journey. It’s easy, intuitive, and just the beginning of your transformation!
                    </p>
                </>
            ),
        },
        2: {
            title: 'Finding Resources',
            image: '/images/getting-started.jpg',
            content: (
                <>
                    <p>
                        Mentorships, scholarships, internships, oh my! Don’t let all the options overwhelm you. Here’s how to find the gems:
                    </p>
                    <ol>
                        <li>
                            <strong>Mentorships That Match:</strong> Use the mentor search tool to find experts aligned with your goals. Filters make it easy to focus on skills or industries that matter to you.
                        </li>
                        <li>
                            <strong>Scholarships Simplified:</strong> Browse curated scholarships based on your background and aspirations. No more endless Google searches!
                        </li>
                        <li>
                            <strong>Internship Goldmines:</strong> Opportunities await. Apply directly or bookmark them for later. (Pro tip: Reach out to your mentor for interview tips!)
                        </li>
                    </ol>
                    <p>
                        Finding resources doesn’t have to feel like searching for a needle in a haystack. We’ve organized everything to keep your experience smooth and seamless.
                    </p>
                </>
            ),
        },
        3: {
            title: 'Maximizing Benefits',
            image: '/images/maximizing-benefits.png',
            content: (
                <>
                    <p>
                        Make the most out of the platform by unlocking its full potential. Here’s how:
                    </p>
                    <ol>
                        <li>
                            <strong>Earning Credits:</strong> Participate in platform challenges, mentor sessions, or contribute helpful tips to earn credits. Use these to access premium content.
                        </li>
                        <li>
                            <strong>Premium Content Perks:</strong> From in-depth guides to exclusive workshops, premium resources take your financial knowledge to the next level.
                        </li>
                        <li>
                            <strong>Stay Informed:</strong> Subscribe to alerts for scholarships, internships, or webinars tailored to your interests. Stay one step ahead of the game.
                        </li>
                    </ol>
                    <p>
                        The Financial Literacy Marketplace is designed to reward engagement and empower users. Get involved and watch your financial literacy soar!
                    </p>
                </>
            ),
        },
    };

    const article = articleContent[articleId];

    if (!article) {
        return <p>Article not found!</p>;
    }

    return (
        <div className="article-page">
            <h1 className="article-title">{article.title}</h1>
            <img src={article.image} alt={article.title} className="article-page-image" />
            <div className="article-content">{article.content}</div>
        </div>
    );
};

export default ArticlePage;

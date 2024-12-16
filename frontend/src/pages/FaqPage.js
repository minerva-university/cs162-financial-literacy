import React, { useState } from 'react';
import { FaChevronDown, FaChevronUp } from 'react-icons/fa';
import '../styles/FAQ.css';

const FaqPage = () => {
    const [activeIndex, setActiveIndex] = useState(null);

    const faqs = [
        {
            question: 'What is the Financial Literacy Marketplace?',
            answer:
                'The Financial Literacy Marketplace is a community-driven platform designed to help you navigate your financial journey. From exploring curated resources and scholarships to booking mentorship sessions, we connect you with the tools and guidance you need to boost your financial confidence.'
        },
        {
            question: 'How do I earn credits?',
            answer:
                'You automatically receive 100 credits as a sign-up bonus. After that, you can earn more by posting content (+3 credits per post) or mentoring others (+10 credits per session). These credits help you access advanced resources and book mentorship sessions without spending real money.'
        },
        {
            question: 'How do I spend credits?',
            answer:
                'Credits function as a virtual currency. Accessing most content costs -0.5 credits per item, and booking a mentorship session costs -10 credits. This ensures a fair and collaborative environment, encouraging active participation and knowledge-sharing.'
        },
        {
            question: 'How can I find and book a mentor?',
            answer:
                'Head over to the Mentors section to browse profiles, each featuring qualifications, availability, and areas of expertise. Once you find a mentor who fits your needs, select a time slot from their calendar, confirm the session with your credits, and you’re all set!'
        },
        {
            question: 'Can I become a mentor?',
            answer:
                'Absolutely! If you have financial expertise to share—be it budgeting, investing, or navigating scholarships—apply on our Mentor Application page. After a review, you can start guiding others and earning credits by helping them succeed.'
        },
        {
            question: 'What are the benefits of mentorship?',
            answer:
                'Mentorship gives you personalized guidance tailored to your goals. Whether you’re new to investing or want to optimize your budgeting, mentors offer actionable insights and moral support, helping you make confident financial decisions.'
        },
        {
            question: 'Is my personal information secure?',
            answer:
                'Your privacy is our priority. We encrypt all personal data and follow strict data protection guidelines. You can trust that your information remains safe and confidential on our platform.'
        },
        {
            question: 'Can I use this platform on my phone or tablet?',
            answer:
                'Yes! The platform is fully responsive, allowing you to access resources, mentors, and your account from any device—smartphone, tablet, or desktop. Learn on the go whenever it’s convenient.'
        },
        {
            question: 'Is the platform free?',
            answer:
                'Signing up and exploring basic features is free. You’ll have an initial set of credits to get started. To access more premium content or mentorship sessions, earn credits by participating or buy them directly for immediate access.'
        }
    ];

    const toggleFaq = (index) => {
        setActiveIndex(activeIndex === index ? null : index);
    };

    return (
        <div className="faq-page">
            <div className="faq-hero">
                <h1 className="faq-title">Frequently Asked Questions</h1>
                <p className="faq-description">
                    Wondering how to navigate our platform? Explore the answers below to learn more 
                    about credits, mentorships, and ways to make the most of your financial literacy journey.
                </p>
            </div>
            <div className="faq-list">
                {faqs.map((faq, index) => (
                    <div
                        key={index}
                        className={`faq-item ${activeIndex === index ? 'active' : ''}`}
                    >
                        <div className="faq-question" onClick={() => toggleFaq(index)}>
                            <span className="question-text">{faq.question}</span>
                            {activeIndex === index ? (
                                <FaChevronUp className="faq-icon" />
                            ) : (
                                <FaChevronDown className="faq-icon" />
                            )}
                        </div>
                        {activeIndex === index && <div className="faq-answer">{faq.answer}</div>}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FaqPage;

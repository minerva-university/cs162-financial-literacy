import React from 'react';
import { FaQuestionCircle } from 'react-icons/fa';
import '../styles/InfoPages.css';


const FaqPage = () => {
    const faqs = [
        {
            question: 'What is Financial Literacy Marketplace?',
            answer:
                'Financial Literacy Marketplace is a platform connecting mentors with mentees for financial education and guidance.',
        },
        {
            question: 'How do I book a mentorship session?',
            answer: 'Simply navigate to the Mentors page, choose a mentor, and book a session!',
        },
        {
            question: 'Is this platform free to use?',
            answer: 'Yes, basic access is free. Additional mentorship services may require credits.',
        },
    ];

    return (
        <div className="info-page">
            <h1 className="info-page-title">FAQ</h1>
            <p className="info-page-description">
                Here are answers to some common questions about our platform.
            </p>
            <div className="faq-list">
                {faqs.map((faq, index) => (
                    <div key={index} className="faq-item">
                        <FaQuestionCircle className="faq-icon" />
                        <div>
                            <h2>{faq.question}</h2>
                            <p>{faq.answer}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FaqPage;

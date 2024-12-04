import React, { useState } from 'react';
import { FaChevronDown, FaChevronUp } from 'react-icons/fa';
import '../styles/FAQ.css';

const FaqPage = () => {
    const [activeIndex, setActiveIndex] = useState(null);

    const faqs = [
        {
            question: 'What is Financial Literacy Marketplace',
            answer:
                'The Financial Literacy Marketplace is an innovative platform connecting individuals with mentors who provide personalized guidance on financial topics. It aims to help users build essential skills such as budgeting, saving, investing, and understanding credit. Additionally, the platform offers curated resources, interactive tools, and community-driven content to create a comprehensive learning experience.',
        },
        {
            question: 'How do I book a mentorship session',
            answer:
                'To book a mentorship session, visit the Mentors page on the platform. Browse through the available mentors, select one based on your preferences, and choose a date and time for the session. The platform provides a seamless booking process to make it easy for you to connect with financial experts.',
        },
        {
            question: 'Is this platform free to use',
            answer:
                'Access to the platform is free for basic features. However, advanced services, including mentorship sessions and exclusive resources, may require credits. These credits can be earned through various activities or purchased directly on the platform.',
        },
        {
            question: 'How do I earn credits',
            answer:
                'Credits can be earned by engaging with the platform through activities such as completing tasks, sharing reviews, or referring new users. Additionally, credits can be purchased for immediate access to premium features and mentorship sessions.',
        },
        {
            question: 'Can I become a mentor',
            answer:
                'If you have financial expertise, you can apply to become a mentor on the platform through the Mentor Application page. The team will review your application based on your qualifications and expertise, ensuring you are the right fit to guide others.',
        },
        {
            question: 'What are the benefits of mentorship',
            answer:
                'Mentorship provides an opportunity to receive personalized financial guidance, tailored to your unique needs and goals. It helps build confidence in managing finances and enables you to make informed decisions about saving, investing, and budgeting.',
        },
        {
            question: 'How secure is my personal information',
            answer:
                'The platform prioritizes user privacy and data security. All personal information is encrypted and stored securely. We adhere to strict data protection guidelines to ensure your information remains safe and confidential.',
        },
        {
            question: 'Can I access the platform on mobile devices',
            answer:
                'Yes, the Financial Literacy Marketplace is fully responsive and can be accessed on any device, including smartphones, tablets, and desktops. This ensures that you can learn and connect with mentors anytime, anywhere.',
        },
    ];

    const toggleFaq = (index) => {
        setActiveIndex(activeIndex === index ? null : index);
    };

    return (
        <div className="faq-page">
            <h1 className="faq-title">Frequently Asked Questions</h1>
            <p className="faq-description">
                Your questions, answered. Explore how the platform can support your financial journey.
            </p>
            <div className="faq-list">
                {faqs.map((faq, index) => (
                    <div
                        key={index}
                        className={`faq-item ${activeIndex === index ? 'active' : ''}`}
                        onClick={() => toggleFaq(index)}
                    >
                        <div className="faq-question">
                            <span>{faq.question}</span>
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

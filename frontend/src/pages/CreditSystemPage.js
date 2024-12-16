import React from 'react';
import '../styles/CreditSystemPage.css';

const CreditSystemPage = () => {
    return (
        <div className="credit-system-container">
            {/* Title and Introduction */}
            <div className="credit-system-header">
                <h1>Understanding the Credit System</h1>
                <p>
                    The credit system is a virtual currency designed to reward active participation
                    and contributions within the Financial Literacy Marketplace. It ensures fair
                    access to resources and fosters a collaborative community.
                </p>
            </div>

            {/* Cards Section */}
            <div className="card-grid">
                <div className="credit-system-card">
                    <div className="credit-system-icon">💰</div>
                    <h2>Why a Credit System?</h2>
                    <p>
                        The credit system encourages user-generated content, enhances engagement, and
                        ensures equal access to resources without monetary transactions.
                    </p>
                </div>
                <div className="credit-system-card">
                    <div className="credit-system-icon">🤝</div>
                    <h2>How to Earn Credits</h2>
                    <p>
                        Post content: <strong>+3 credits</strong> per post<br />
                        Mentor others: <strong>+10 credits</strong> per session
                    </p>
                </div>
                <div className="credit-system-card">
                    <div className="credit-system-icon">🔄</div>
                    <h2>How to Spend Credits</h2>
                    <p>
                        Access content: <strong>-0.5 credits</strong> per item<br />
                        Book mentorship: <strong>-10 credits</strong> per session
                    </p>
                </div>
            </div>

            {/* Table Section */}
            <div className="credit-system-summary">
                <h2>Credit Values for Actions</h2>
                <table className="credit-table">
                    <thead>
                        <tr>
                            <th>Action</th>
                            <th>Credits Gained</th>
                            <th>Credits Spent</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Sign-up Bonus</td>
                            <td>+100</td>
                            <td>-</td>
                        </tr>
                        <tr>
                            <td>Post Content</td>
                            <td>+3</td>
                            <td>-</td>
                        </tr>
                        <tr>
                            <td>Mentor Others</td>
                            <td>+10</td>
                            <td>-</td>
                        </tr>
                        <tr>
                            <td>Access Content</td>
                            <td>-</td>
                            <td>-0.5</td>
                        </tr>
                        <tr>
                            <td>Book Mentorship</td>
                            <td>-</td>
                            <td>-10</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default CreditSystemPage;

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import ProfilePage from './pages/ProfilePage';
import Signup from './pages/Signup';
import Login from './pages/Login';
import MainPage from './pages/MainPage';
import LandingPage from './pages/LandingPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './index.css';
import PostFeed from './components/Feed';
import PostForm from './components/PostForm';
import { is_authenticated } from './services/api';
import PostPage from './components/Post';
import WhyChooseUsPage from './pages/WhyChooseUsPage';
import MentorsListPage from './pages/MentorsListPage';
import AboutUsPage from './pages/AboutUsPage';
import ContactUsPage from './pages/ContactUsPage';
import FaqPage from './pages/FaqPage';
import ArticlesPage from './pages/ArticlesPage';
import ArticlePage from './pages/ArticlePage';
import { MentorshipProvider } from './pages/MentorshipContext';
import MentorshipSessionsPage from './pages/MentorshipSessionsPage';
import MentorshipHistoryPage from './pages/MentorshipHistoryPage';
import FeedPage from './pages/FeedPage';
import OtherProfile from './pages/OtherProfile';
import CreditSystemPage from './pages/CreditSystemPage';
import ScholarshipsPage from './pages/ScholarshipsPage';
import InternshipsPage from './pages/InternshipsPage';

function App() {
    const [authenticated, setAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    const handleLogout = () => {
        localStorage.setItem("logged", "false");
        setAuthenticated(false);
    };

    useEffect(() => {
        const checkAuthentication = async () => {
            try {
                const authenticated = await is_authenticated();
                setAuthenticated(authenticated);
                localStorage.setItem("logged", authenticated ? "true" : "false");
            } catch (error) {
                console.error('Error during authentication check:', error);
                setAuthenticated(false);
            } finally {
                setLoading(false); // Ensure app does not navigate prematurely
            }
        };

        checkAuthentication();
    }, []);

    if (loading) {
        // Prevent rendering until authentication check is complete
        return <div>Loading...</div>;
    }

    return (
        <Router>
            <div className="min-h-screen flex flex-col">
                <Routes>
                    {/* Routes for unauthenticated users */}
                    {!authenticated ? (
                        <>
                            <Route path="/" element={<LandingPage />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/signup" element={<Signup />} />
                            <Route path="/about" element={<AboutUsPage />} />
                            <Route path="/contact" element={<ContactUsPage />} />
                            <Route path="/faq" element={<FaqPage />} />
                            <Route path="/articles" element={<ArticlesPage />} />
                            <Route path="/article/:articleId" element={<ArticlePage />} />
                            {/* Redirect unauthenticated users to landing page */}
                            <Route path="*" element={<Navigate to="/" />} />
                        </>
                    ) : (
                        <>
                            {/* Routes for authenticated users */}
                            <Route
                                path="/*"
                                element={
                                    <>
                                        <Navbar onLogout={handleLogout} />
                                        <main className="flex-grow">
                                            <MentorshipProvider>
                                                <Routes>
                                                    <Route path="/home" element={<MainPage />} />
                                                    <Route path="/mentors" element={<MentorsListPage />} />
                                                    <Route path="/mentorship/upcoming" element={<MentorshipSessionsPage />} />
                                                    <Route path="/mentorship/history" element={<MentorshipHistoryPage />} />
                                                    <Route path="/post" element={<PostForm />} />
                                                    <Route path="/feed" element={<FeedPage />} />
                                                    <Route path="/profile" element={<ProfilePage />} />
                                                    <Route path="/post/:postId" element={<PostPage />} />
                                                    <Route path="/user/:userId" element={<OtherProfile />} />
                                                    <Route path="/why-choose-us" element={<WhyChooseUsPage />} />
                                                    <Route path="/credits" element={<CreditSystemPage />} />
                                                    <Route path="/scholarships" element={<ScholarshipsPage />} />
                                                    <Route path="/internships" element={<InternshipsPage />} />
                                                    <Route path="/about" element={<AboutUsPage />} />
                                                    <Route path="/contact" element={<ContactUsPage />} />
                                                    <Route path="/faq" element={<FaqPage />} />
                                                    <Route path="/articles" element={<ArticlesPage />} />
                                                    <Route path="/article/:articleId" element={<ArticlePage />} />
                                                    {/* Redirect authenticated users to main page */}
                                                    <Route path="*" element={<Navigate to="/home" />} />
                                                </Routes>
                                            </MentorshipProvider>
                                        </main>
                                        <Footer />
                                    </>
                                }
                            />
                        </>
                    )}
                </Routes>
            </div>
        </Router>
    );
}

export default App;

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProfilePage from './pages/ProfilePage';
import Signup from './pages/Signup';
import Login from './pages/Login';
import MainPage from './pages/MainPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './index.css';
import PostFeed from './pages/Feed';
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

function App() {
    useEffect(() => {
        const checkAuthentication = async () => {
            const authenticated = await is_authenticated();

            if (!authenticated) {
                localStorage.setItem("logged", "false");
                if (
                    window.location.pathname !== "/login" &&
                    window.location.pathname !== "/signup"
                ) {
                    window.location.href = "/login";
                }
            } else {
                localStorage.setItem("logged", "true");
            }
        };

        checkAuthentication();
    }, []);

    return (
        <Router>
            <div className="min-h-screen flex flex-col">
                <Navbar />
                <main className="flex-grow">
                    <Routes>
                        <Route path="/" element={<MainPage />} />
                        <Route path="/mentors" element={<MentorsListPage />} />
                        <Route path="/post" element={<PostForm />} />
                        <Route path="/feed" element={<PostFeed />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/profile" element={<ProfilePage />} />
                        <Route path="/post/:postId" element={<PostPage />} />
                        <Route path="/why-choose-us" element={<WhyChooseUsPage />} />
                        <Route path="/about" element={<AboutUsPage />} />
                        <Route path="/contact" element={<ContactUsPage />} />
                        <Route path="/faq" element={<FaqPage />} />
                        <Route path="/articles" element={<ArticlesPage />} />
                        <Route path="/article/:articleId" element={<ArticlePage />} />
                    </Routes>
                </main>
                <Footer />
            </div>
        </Router>
    );
}

export default App;

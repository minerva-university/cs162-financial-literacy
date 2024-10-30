// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProfilePage from './pages/ProfilePage';
import Signup from './pages/Signup';
import Login from './pages/Login';
import MainPage from './pages/MainPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer'; // Assuming Footer component is used globally

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/login" element={<Login />} />
                <Route path="/profile" element={<ProfilePage />} />
                {/* Add more routes as needed */}
            </Routes>
            <Footer /> {/* Footer will be shown on all pages */}
        </Router>
    );
}

export default App;

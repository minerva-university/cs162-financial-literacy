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

function App() {

    useEffect(async ()=>{
        const authenticated = await is_authenticated()
        
          if(authenticated){
            localStorage.setItem("logged", "false")
            
          } else {
            localStorage.setItem("logged", "true")
          }
    
          if(!authenticated && (window.location.pathname != "/login"&&window.location.pathname != "/signup")){
            
            window.location.href = "/login"
            console.log(window.path)
            
          } 
    
          
        
      }, [])
    return (
        <Router>
            <div className="min-h-screen flex flex-col">
                <Navbar />
                <main className="min-h-screen">
                    <Routes>
                        <Route path="/" element={<MainPage />} />
                        <Route path="/post" element={<PostForm />} />
                        <Route path="/feed" element={<PostFeed />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/profile" element={<ProfilePage />} />
                        <Route path="/post/:postId"  element={<PostPage />} /> 
                    </Routes>
                </main>
                <Footer />
            </div>
        </Router>
    );
}

export default App;
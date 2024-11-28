// src/components/Navbar.js

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { is_authenticated, logout } from '../services/api';

const Navbar = () => {
    const [authenticated, setauthenticated] = useState(false)

    async function handlelogout(){
        await logout();
        window.location.href = "/login";
    };
    
    useEffect(async ()=>{
        setauthenticated(await is_authenticated())
    }, [])
    return (
        <nav className="bg-gray-800 text-white">
            <ul className="flex justify-between items-center py-4 px-8 max-w-[500px] mx-auto">
                {authenticated&&<li className="hidden md:block">
                    <Link to="/profile" className="hover:text-gray-300">Profile</Link>
                </li>}
                {authenticated&&<li>
                    <Link to="/" className="font-bold text-lg">Home</Link>
                </li>}
                {!authenticated&&<li className="hidden md:block">
                    <Link to="/signup" className="hover:text-gray-300">Signup</Link>
                </li>}
                {!authenticated&&<li className="hidden md:block">
                    <Link to="/login" className="hover:text-gray-300">Login</Link>
                </li>}
                
                {authenticated&&<li>
                    <button onClick={handlelogout} className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                        Logout
                    </button>
                </li>}
            </ul>
        </nav>
    );
};

export default Navbar;

// src/components/Navbar.js

import React, { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
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
        <nav class="bg-gray-800 text-white">
            <ul class="flex justify-between items-center py-4 px-8">
                {authenticated&&<li>
                    <Link to="/" class="font-bold text-lg">Home</Link>
                </li>}
                {!authenticated&&<li class="hidden md:block">
                    <Link to="/signup" class="hover:text-gray-300">Signup</Link>
                </li>}
                {!authenticated&&<li class="hidden md:block">
                    <Link to="/login" class="hover:text-gray-300">Login</Link>
                </li>}
                {authenticated&&<li class="hidden md:block">
                    <Link to="/profile" class="hover:text-gray-300">Profile</Link>
                </li>}
                {authenticated&&<li>
                    <button onClick={handlelogout} class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Logout
                    </button>
                </li>}
            </ul>
        </nav>
    );
};

export default Navbar;
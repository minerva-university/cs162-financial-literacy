import React, { useState, useEffect } from 'react';
import { FaIdBadge, FaUser, FaUserEdit } from 'react-icons/fa';
import { getUserProfile, updateUserName, updateMentorship, getPostsCurrentUser, getPostsByUser, getOtherProfile } from '../services/api';
import '../styles/ProfilePage.css';
import PostFeed from '../components/Feed';
import { useParams } from 'react-router-dom';

const OtherProfile = () => {
  const [userData, setUserData] = useState(null);
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const {userId} = useParams()

  useEffect(() => {

    const fetchPosts = async () => {
      try {
        setPosts(await getPostsByUser(userId));
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, []);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profile = await getOtherProfile(userId);
        setUserData(profile);
      } catch (error) {
        console.error("Failed to fetch profile", error);
      }
    };
    fetchProfile();
  }, []);

  

  if (!userData) return <div className="loading">Loading profile...</div>;

  return (
    <div className="profile-page">
      <h2 className="profile-header">{userData.name}'s Profile</h2>
      <div className="profile-card">
        <div className="profile-section">
          <FaIdBadge className="profile-icon" />
          <span className="label">ID:</span>
          <span className="value">{userData.id}</span>
        </div>
        <div className="profile-section">
          <FaIdBadge className="profile-icon" />
          <span className="label">Email:</span>
          <span className="value">{userData.email}</span>
        </div>
        <div className="profile-section">
          <FaUser className="profile-icon" />
          <span className="label">Name:</span>
          <span className="value">{userData.name}</span>
        </div>
        <div className="profile-section">
          <span className="label">Mentorship Availability:</span>
          <select
            value={userData.mentorship}
            disabled
            className="availability-select"
          >
            <option value="yes">Available</option>
            <option value="no">Not Available</option>
          </select>
        </div>
      </div>
      <div className='my-4'>
        <h2 className="profile-header">{userData.name}'s Posts</h2>
        {posts.length>0&&<>
          <PostFeed posts={posts} isLoading={isLoading} error={error} deleteOption={false}/>
        </>||<div className=' text-center'> {userData.name} never posted! </div>}
      </div>

    </div>
  );
};

export default OtherProfile;

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaIdBadge, FaUser, FaUserEdit } from 'react-icons/fa';
import {
  getUserProfile,
  updateUserName,
  updateMentorship,
  getPostsCurrentUser,
} from '../services/api';
import '../styles/ProfilePage.css';
import PostFeed from '../components/Feed';
import MentorshipRequest from '../components/MentorshipReqeust';

const ProfilePage = () => {
  const [userData, setUserData] = useState(null);
  const [isEditingName, setIsEditingName] = useState(false);
  const [newName, setNewName] = useState('');
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const userPosts = await getPostsCurrentUser();
        setPosts(userPosts);
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
        const profile = await getUserProfile();
        setUserData(profile);
      } catch (error) {
        console.error('Failed to fetch profile', error);
      }
    };
    fetchProfile();
  }, []);

  const handleMentorshipChange = async (event) => {
    const availability = event.target.value;
    try {
      const result = await updateMentorship(availability);
      if (result.success) {
        setUserData({ ...userData, mentorship_availability: availability });
        alert(
          `Mentorship availability updated to: ${
            availability === 'yes' ? 'Available' : 'Not Available'
          }`
        );
      } else {
        alert('Failed to update mentorship availability. Please try again.');
      }
    } catch (error) {
      console.error('Mentorship update error', error);
      alert('An error occurred. Please try again.');
    }
  };

  const handleSaveName = async () => {
    try {
      const result = await updateUserName(newName);
      if (result.success) {
        setUserData({ ...userData, name: newName });
        alert('Name updated successfully!');
        setIsEditingName(false);
      } else {
        alert('Failed to update name. Please try again.');
      }
    } catch (error) {
      console.error('Name update error', error);
      alert('An error occurred. Please try again.');
    }
  };

  if (!userData) return <div className="loading">Loading profile...</div>;

  return (
    <div className="profile-page-container">
      {/* Profile Section */}
      <div className="profile-card">
        <h2>Profile</h2>
        <div className="profile-info">
          <div className="info-item">
            <FaIdBadge className="profile-icon" />
            <span>ID: {userData.id}</span>
          </div>
          <div className="info-item">
            <FaUser className="profile-icon" />
            <span>Name: {userData.name}</span>
            <button
              className="edit-button"
              onClick={() => setIsEditingName(true)}
            >
              <FaUserEdit />
            </button>
          </div>
          {isEditingName && (
            <div className="edit-name-section">
              <input
                type="text"
                placeholder="Enter new name"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                className="edit-name-input"
              />
              <button className="save-button" onClick={handleSaveName}>
                Save
              </button>
              <button
                className="cancel-button"
                onClick={() => setIsEditingName(false)}
              >
                Cancel
              </button>
            </div>
          )}
          <div className="info-item">
            <span>Mentorship Availability:</span>
            <select
              value={userData.mentorship_availability}
              onChange={handleMentorshipChange}
              className="availability-select"
            >
              <option value="yes">Available</option>
              <option value="no">Not Available</option>
            </select>
          </div>
        </div>
      </div>

      {/* Posts Section */}
      <div className="posts-section">
        <div className="posts-header">
          <h2 className="posts-title">My Posts</h2>
          <button
            className="create-post-button"
            onClick={() => navigate('/post')}
          >
            + Create Post
          </button>
        </div>
        {isLoading ? (
          <p>Loading posts...</p>
        ) : posts.length > 0 ? (
          <div className="posts-feed">
            {posts.map((post) => (
              <div key={post.id} className="post-card">
                <h3 className="post-title">{post.title}</h3>
                <p className="post-content">{post.content}</p>
                <p className="post-meta">
                  <span>Author: {post.author}</span> |{' '}
                  <span>Created: {post.created_at}</span>
                </p>
                <button className="delete-button">Delete</button>
              </div>
            ))}
          </div>
        ) : (
          <p>No posts yet. Create your first post now!</p>
        )}
      </div>

      {/* Mentorship Request Section */}
      <MentorshipRequest />
    </div>
  );
};

export default ProfilePage;

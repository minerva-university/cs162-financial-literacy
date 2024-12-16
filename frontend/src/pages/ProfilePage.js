import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaIdBadge, FaUser, FaUserEdit, FaInfoCircle } from "react-icons/fa";
import {
  getUserProfile,
  updateUserName,
  updateMentorship,
  getPostsCurrentUser,
  updateUserBio,
} from "../services/api";
import "../styles/ProfilePage.css";
import MentorshipRequest from "../components/MentorshipReqeust";
import PostFeed from "../components/Feed";

const ProfilePage = () => {
  const [userData, setUserData] = useState(null);
  const [isEditingName, setIsEditingName] = useState(false);
  const [isEditingBio, setIsEditingBio] = useState(false);
  const [newName, setNewName] = useState("");
  const [newBio, setNewBio] = useState("");
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Fetch Posts
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

  // Fetch User Profile
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profile = await getUserProfile();
        setUserData(profile);
        setNewBio(profile.bio || ""); // Set initial bio value
      } catch (error) {
        console.error("Failed to fetch profile", error);
      }
    };
    fetchProfile();
  }, []);

  // Handle Mentorship Availability Change
  const handleMentorshipChange = async (event) => {
    const availability = event.target.value;
    try {
      const result = await updateMentorship(availability);
      if (result.status) {
        setUserData({ ...userData, mentorship_availability: availability });
        alert(
          `Mentorship availability updated to: ${
            availability === "yes" ? "Available" : "Not Available"
          }`
        );
      } else {
        alert("Failed to update mentorship availability. Please try again.");
      }
    } catch (error) {
      console.error("Mentorship update error", error);
      alert("An error occurred. Please try again.");
    }
  };

  // Handle Save Name
  const handleSaveName = async () => {
    try {
      const result = await updateUserName(newName);
      if (result.success) {
        setUserData({ ...userData, name: newName });
        alert("Name updated successfully!");
        setIsEditingName(false);
      } else {
        alert("Failed to update name. Please try again.");
      }
    } catch (error) {
      console.error("Name update error", error);
      alert("An error occurred. Please try again.");
    }
  };

  // Handle Save Bio
  const handleSaveBio = async () => {
    try {
      const result = await updateUserBio(newBio); // Call new API function
      if (result.success) {
        setUserData({ ...userData, bio: result.bio });
        alert("Bio updated successfully!");
        setIsEditingBio(false);
      } else {
        alert("Failed to update bio: " + result.message);
      }
    } catch (error) {
      console.error("Error updating bio", error);
      alert("An error occurred while updating your bio.");
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
            <FaInfoCircle className="profile-icon" />
            <span>Bio: {userData.bio || "No bio added yet"}</span>
            <button
              className="edit-button"
              onClick={() => setIsEditingBio(true)}
            >
              <FaUserEdit />
            </button>
          </div>
          <div className="info-item">
            <span>Credits:</span>
            <span className="credits-value">{userData.credits || 0}</span>
          </div>

          {isEditingBio && (
            <div className="edit-bio-section">
              <textarea
                placeholder="Enter your bio"
                value={newBio}
                onChange={(e) => setNewBio(e.target.value)}
                className="edit-bio-input"
              />
              <button className="save-button" onClick={handleSaveBio}>
                Save
              </button>
              <button
                className="cancel-button"
                onClick={() => setIsEditingBio(false)}
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
            onClick={() => navigate("/post")}
          >
            + Create Post
          </button>
        </div>
        {isLoading ? (
          <p>Loading posts...</p>
        ) : posts.length > 0 ? (
          <PostFeed posts={posts} setPosts={setPosts} isLoading={isLoading} error={error} deleteOption={true} />
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

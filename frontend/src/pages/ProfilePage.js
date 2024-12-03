import React, { useState, useEffect } from 'react';
import { FaIdBadge, FaUser, FaUserEdit } from 'react-icons/fa';
import { getUserProfile, updateUserName, updateMentorship } from '../services/api';
import '../styles/ProfilePage.css';

const ProfilePage = () => {
  const [userData, setUserData] = useState(null);
  const [isEditingName, setIsEditingName] = useState(false);
  const [newName, setNewName] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profile = await getUserProfile();
        setUserData(profile);
      } catch (error) {
        console.error("Failed to fetch profile", error);
      }
    };
    fetchProfile();
  }, []);

  const handleMentorshipChange = async (event) => {
    const availability = event.target.value;
    try {
      const result = await updateMentorship(availability);
      if (result.success) {
        setUserData({ ...userData, mentorship: availability });
        alert(`Mentorship availability updated to: ${availability === 'yes' ? 'Available' : 'Not Available'}`);
      } else {
        alert('Failed to update mentorship availability. Please try again.');
      }
    } catch (error) {
      console.error("Mentorship update error", error);
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
    <div className="profile-page">
      <h2 className="profile-header">Your Profile</h2>
      <p className="profile-subheader">Manage your account details and preferences below.</p>
      <div className="profile-card">
        <div className="profile-section">
          <FaIdBadge className="profile-icon" />
          <span className="label">ID:</span>
          <span className="value">{userData.id}</span>
        </div>
        <div className="profile-section">
          <FaUser className="profile-icon" />
          <span className="label">Name:</span>
          <span className="value">{userData.name}</span>
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
        <div className="profile-section">
          <span className="label">Mentorship Availability:</span>
          <select
            value={userData.mentorship}
            onChange={handleMentorshipChange}
            className="availability-select"
          >
            <option value="yes">Available</option>
            <option value="no">Not Available</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;

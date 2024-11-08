// src/pages/ProfilePage.js

import React, { useState, useEffect } from 'react';
import EditUserNameModal from '../components/EditUserNameModal';
import { getUserProfile, updateUserName, updateMentorship } from '../services/api';

const ProfilePage = () => {
  const [userData, setUserData] = useState(null);
  const [isEditingName, setIsEditingName] = useState(false);

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

  if (!userData) return <div>Loading profile...</div>;

  return (
    <div>
      <h2>User Profile</h2>
      <h3>ID: {userData.id}</h3>
      <h3>Name: {userData.name}</h3>
      <button onClick={() => setIsEditingName(true)}>Edit Name</button>
      
      <div>
        <label>
          Mentorship Availability:
          <select value={userData.mentorship} onChange={handleMentorshipChange}>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </label>
      </div>

      {isEditingName && (
        <EditUserNameModal
          userData={userData}
          setUserData={setUserData}
          closeModal={() => setIsEditingName(false)}
        />
      )}
    </div>
  );
};

export default ProfilePage;

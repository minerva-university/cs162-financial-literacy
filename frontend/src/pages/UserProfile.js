import React, { useState, useEffect } from 'react';
import EditUserNameModal from '../components/EditUserNameModal';
import { getUserProfile, updateMentorship } from '../services/api';



const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const [isEditingName, setIsEditingName] = useState(false);
  

  useEffect(() => {
    const fetchUserProfile = async () => {
      const data = await getUserProfile();
      setUserData(data);
    };
    fetchUserProfile();
  }, []);

  const handleMentorshipChange = async (event) => {
    const availability = event.target.value;
    const result = await updateMentorship(availability);
    if (result.success) {
      setUserData({ ...userData, mentorship: availability });
      alert(`Your mentorship availability is now set to: ${availability === 'yes' ? 'Available' : 'Not Available'}`);
    } else {
      alert('Failed to update mentorship availability. Please try again.');
    }
  };

  return userData ? (
    <div>
      <h2>User ID: {userData.id}</h2>
      <h3>User Name: {userData.name}</h3>
      <button onClick={() => setIsEditingName(true)}>Change User Name</button>
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
  ) : <p>Loading...</p>;
};

export default UserProfile;

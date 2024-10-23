import React, { useState } from 'react';
import EditUserNameModal from './EditUserNameModal';
import { updateMentorship } from '../services/api';

const UserProfile = ({ userData, setUserData }) => {
  const [isEditingName, setIsEditingName] = useState(false);

  const handleMentorshipChange = async (event) => {
    const availability = event.target.value;
    const result = await updateMentorship(availability);
    if (result.success) {
      setUserData({ ...userData, mentorship: availability });
    }
  };

  return (
    <div>
      <h2>User ID: {userData.id}</h2>
      <h3>User Name: {userData.name}</h3>
      <button onClick={() => setIsEditingName(true)}>Change User Name</button>
      
      <div>
        <label>
          Mentorship Availability:
          <select
            value={userData.mentorship}
            onChange={handleMentorshipChange}
          >
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

export default UserProfile;

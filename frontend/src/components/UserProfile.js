import React, { useState } from 'react';
import EditUserNameModal from './EditUserNameModal';
import { updateMentorship } from '../services/api';

const UserProfile = ({ userData, setUserData }) => {
  const [isEditingName, setIsEditingName] = useState(false);
  const [mentorshipStatus, setMentorshipStatus] = useState(userData.mentorship);

  const handleMentorshipChange = async (event) => {
    const availability = event.target.value;
    const result = await updateMentorship(availability);
    if (result.success) {
      setUserData({ ...userData, mentorship: availability });
      setMentorshipStatus(availability);
      alert(`Your mentorship availability is now set to: ${availability === 'yes' ? 'Available' : 'Not Available'}`);
    } else {
      alert('Failed to update mentorship availability. Please try again.');
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
            value={mentorshipStatus}
            onChange={handleMentorshipChange}
          >
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </label>
      </div>

      <div>
        <label>School:</label>
        <input
          type="text"
          value={userData.school || ''}
          onChange={(e) => setUserData({ ...userData, school: e.target.value })}
        />
      </div>
      <div>
        <label>Company:</label>
        <input
          type="text"
          value={userData.company || ''}
          onChange={(e) => setUserData({ ...userData, company: e.target.value })}
        />
      </div>
      <div>
        <label>Role:</label>
        <input
          type="text"
          value={userData.role || ''}
          onChange={(e) => setUserData({ ...userData, role: e.target.value })}
        />
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

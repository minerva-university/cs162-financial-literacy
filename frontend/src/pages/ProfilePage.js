import React, { useState, useEffect } from 'react';
import UserProfile from '../components/UserProfile';
import MyPostingsPreview from '../components/MyPostingsPreview';
import { getUserProfile, getUserPostings } from '../services/api';

const ProfilePage = () => {
  const [userData, setUserData] = useState(null);
  const [postings, setPostings] = useState([]);

  useEffect(() => {
    // Fetch user data
    async function fetchData() {
      const profile = await getUserProfile();
      setUserData(profile);

      const userPostings = await getUserPostings();
      setPostings(userPostings);
    }
    fetchData();
  }, []);

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>My Profile</h1>
      <UserProfile userData={userData} setUserData={setUserData} />
      <MyPostingsPreview postings={postings} />
    </div>
  );
};

export default ProfilePage;

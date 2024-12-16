import React, { useState, useEffect } from 'react';
import { FaIdBadge, FaUser, FaUserEdit } from 'react-icons/fa';
import { getPostsByUser, getOtherProfile, isFollowing, followUser, unfollowUser } from '../services/api';
import '../styles/ProfilePage.css';
import PostFeed from '../components/Feed';
import { useParams } from 'react-router-dom';

const OtherProfile = () => {
  const [userData, setUserData] = useState(null);
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [following, setFollowing] = useState(false);
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

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const f = await isFollowing(userId);
        setFollowing(f);
      } catch (error) {
        console.error("Failed to fetch follow status", error);
      }
    };
    fetchProfile();
  }, []);

  

  if (!userData) return <div className="loading">Loading profile...</div>;

  return (
    <div className="grid grid-cols-3 p-5 mx-10">
      
      <div className="profile-card col-span-1">
        <h2 className="profile-header">{userData.name}'s Profile</h2>
        <div className="profile-info">
            <div className="info-item">
              <FaIdBadge className="profile-icon" />
              <span>ID: {userData.id}</span>
            </div>
            <div className="info-item">
              <FaUser className="profile-icon" />
              <span>Name: {userData.name}</span>
            </div>
            
            <div className="info-item">
            <FaIdBadge className="profile-icon" />
            <span className="label">Email:</span>
            <span className="value">{userData.email}</span>
        </div>
        <div className="info-item">
              <span>Mentorship Availability:</span>
              <select
                value={userData.mentorship_availability}
                disabled
                className="availability-select"
              >
                <option value="yes">Available</option>
                <option value="no">Not Available</option>
              </select>
            </div>
        <div className="info-item">
          <span className="value">{following?"Following":"Not following"}</span>
          {following?
          <div className='rounded-xl bg-red-500 p-2'>
            <button onClick={()=>{unfollowUser(userId);setFollowing(false)}}>Unfollow</button>
          </div>
            :
          <div className='rounded-xl bg-green-500 p-2'>
            <button onClick={()=>{followUser(userId);setFollowing(true)}}>Follow</button>
          </div>
        }
        </div>
          </div>

      </div>
      <div className='my-4 col-span-2 '>
        <h2 className="posts-title p-2">{userData.name}'s Posts</h2>
        {posts.length>0&&<>
          <PostFeed posts={posts} setPosts={setPosts} isLoading={isLoading} error={error} deleteOption={false}/>
        </>||<div className=' text-center'> {userData.name} never posted! </div>}
      </div>

    </div>
  );
};

export default OtherProfile;

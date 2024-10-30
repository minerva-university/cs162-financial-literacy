import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Needs to be replaced with backend url

// Get user profile data
export const getUserProfile = async () => {
  const response = await axios.get(`${API_URL}/user/profile`, { withCredentials: true });
  return response.data;
};

// Update user name
export const updateUserName = async (newName) => {
  const response = await axios.post(
    `${API_URL}/user/update-name`,
    { name: newName },
    { withCredentials: true }
  );
  return response.data;
};

// Get user's postings
export const getUserPostings = async () => {
  const response = await axios.get(`${API_URL}/user/my-postings`, { withCredentials: true });
  return response.data;
};

// Update mentorship availability
export const updateMentorship = async (availability) => {
  const response = await axios.post(
    `${API_URL}/user/update-mentorship`,
    { availability },
    { withCredentials: true }
  );
  return response.data;
};

// Fetch available mentors
export const getAvailableMentors = async () => {
  const response = await axios.get(`${API_URL}/mentors/available`, { withCredentials: true });
  return response.data;
};

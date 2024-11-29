import axios from 'axios';

const API_URL = process.env.REACT_APP_backend_api;

// Check Authentication
export const is_authenticated = async () => {
  const response = await axios.get(`${API_URL}/ping`, { withCredentials: true });
  return response.data.authenticated;
};

// Login
export const login = async (email, password, remember) => {
  const response = await axios.post(`${API_URL}/login`, { email, password, remember }, { withCredentials: true });
  return response.data;
};

export const register = async (email, name, password) => {
  const response = await axios.post(`${API_URL}/signup`, { email, name, password }, { withCredentials: true });
  return response.data;
      
};



// Logout
export const logout = async () => {
  const response = await axios.get(`${API_URL}/logout`, { withCredentials: true });
  return response.data;
};

// Get user profile
export const getUserProfile = async () => {
  const response = await axios.get(`${API_URL}/profile`, { withCredentials: true });
  return response.data;
};

// Update user name
export const updateUserName = async (newName) => {
  const response = await axios.post(`${API_URL}/profile`, { name: newName }, { withCredentials: true });
  return response.data;
};

// Update mentorship availability
export const updateMentorship = async (availability) => {
  const response = await axios.post(`${API_URL}/mentors/availability`, { availability }, { withCredentials: true });
  return response.data;
};

// Fetch available mentors
export const getAvailableMentors = async () => {
  const response = await axios.get(`${API_URL}/mentors/available`, { withCredentials: true });
  return response.data;
};

// Add a new post
export const addPost = async (title, content) => {
  const response = await axios.post(`${API_URL}/post`, { title, content }, { withCredentials: true });
  return response.data;
};

// Get all posts
export const getPosts = async () => {
  const response = await axios.get(`${API_URL}/posts`, { withCredentials: true });
  return response.data.posts;
};

// Get a single post
export const getPostById = async (postId) => {
  const response = await axios.get(`${API_URL}/post/${postId}`, { withCredentials: true });
  return response.data;
};


// Upvoting a post
export const vote = async (postId, vote_type) => {
  const response = await axios.post(`${API_URL}/post/${postId}/vote`, {vote_type}, { withCredentials: true });
  return response.data.message;
};

// Commenting on a post
export const comment = async (postId, comment_text) => {
  const response = await axios.post(`${API_URL}/post/${postId}/comment`, {comment_text}, { withCredentials: true });
  return response.data;
};

// Get all scholarships
export const getScholarships = async () => {
  const response = await axios.get(`${API_URL}/scholarships`, { withCredentials: true });
  return response.data;
};

// Post a new scholarship
export const postScholarship = async (title, description, requirements, applicationLink) => {
  const response = await axios.post(`${API_URL}/scholarships`, {
    title,
    description,
    requirements,
    applicationLink
  }, { withCredentials: true });
  return response.data;
};

// Get all internships
export const getInternships = async () => {
  const response = await axios.get(`${API_URL}/internships`, { withCredentials: true });
  return response.data;
};

// Post a new internship
export const postInternship = async (title, description, requirements, applicationLink) => {
  const response = await axios.post(`${API_URL}/internships`, {
    title,
    description,
    requirements,
    applicationLink
  }, { withCredentials: true });
  return response.data;
};

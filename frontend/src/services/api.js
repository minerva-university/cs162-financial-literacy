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

// Register
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

// Book mentorship
export const bookMentorship = async (mentorId, scheduledTime) => {
  const response = await axios.post(`${API_URL}/mentorship/book`, {
    mentor_id: mentorId,
    scheduled_time: scheduledTime
  }, { withCredentials: true });
  return response.data;
};

// Complete mentorship session
export const completeMentorship = async (sessionId) => {
  const response = await axios.post(`${API_URL}/mentorship/complete/${sessionId}`, {}, { withCredentials: true });
  return response.data;
};

// Cancel mentorship session
export const cancelMentorship = async (sessionId) => {
  const response = await axios.post(`${API_URL}/mentorship/cancel/${sessionId}`, {}, { withCredentials: true });
  return response.data;
};

// Get mentorship history
export const getMentorshipHistory = async () => {
  const response = await axios.get(`${API_URL}/mentorship/history`, { withCredentials: true });
  return response.data;
};

// Get upcoming mentorship sessions
export const getUpcomingMentorships = async () => {
  const response = await axios.get(`${API_URL}/mentorship/upcoming`, { withCredentials: true });
  return response.data;
};

// Submit feedback for mentorship session
export const submitFeedback = async (sessionId, feedback) => {
  const response = await axios.post(`${API_URL}/mentorship/feedback/${sessionId}`, {
    feedback: feedback
  }, { withCredentials: true });
  return response.data;
};

// Get user credits
export const getUserCredits = async () => {
  const response = await axios.get(`${API_URL}/mentorship/get_credits`, { withCredentials: true });
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

// Upvote a post
export const vote = async (postId, vote_type) => {
  const response = await axios.post(`${API_URL}/post/${postId}/vote`, { vote_type }, { withCredentials: true });
  return response.data.message;
};

// Comment on a post
export const comment = async (postId, comment_text) => {
  const response = await axios.post(`${API_URL}/post/${postId}/comment`, { comment_text }, { withCredentials: true });
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

// Get scheduled mentorship sessions
export const getScheduledSessions = async () => {
  const response = await axios.get(`${API_URL}/mentorship/upcoming`, { withCredentials: true });
  return response.data;
};

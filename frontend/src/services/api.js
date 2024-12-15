import axios from 'axios';

const API_URL = process.env.REACT_APP_backend_api;

// Authentication
export const is_authenticated = async () => {
  const response = await axios.get(`${API_URL}/ping`, { withCredentials: true });
  return response.data.authenticated;
};

export const login = async (email, password, remember) => {
  const response = await axios.post(`${API_URL}/login`, { email, password, remember }, { withCredentials: true });
  return response.data;
};

export const register = async (email, name, password) => {
  const response = await axios.post(`${API_URL}/signup`, { email, name, password }, { withCredentials: true });
  return response.data;
};

export const logout = async () => {
  const response = await axios.get(`${API_URL}/logout`, { withCredentials: true });
  return response.data;
};

// User Profile
export const getUserProfile = async () => {
  const response = await axios.get(`${API_URL}/profile`, { withCredentials: true });
  return response.data;
};

// Other people's Profile
export const getOtherProfile = async (userId) => {
  const response = await axios.get(`${API_URL}/profile/${userId}`, { withCredentials: true });
  return response.data;
};

export const updateUserName = async (newName) => {
  const response = await axios.post(`${API_URL}/profile`, { name: newName }, { withCredentials: true });
  return response.data;
};

export const getUserCredits = async () => {
  const response = await axios.get(`${API_URL}/mentorship/get_credits`, { withCredentials: true });
  return response.data;
};

// Mentorship APIs
export const updateMentorship = async (availability) => {
  const response = await axios.post(`${API_URL}/mentors/availability`, { availability }, { withCredentials: true });
  return response.data;
};

export const getAvailableMentors = async () => {
  try {
    console.log('API URL:', API_URL);
    const response = await axios.get(`${API_URL}/mentors/available`, { withCredentials: true });
    console.log('Mentors API Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching mentors:', error);
    console.error('Error details:', error.response);
    throw error;
  }
};
export const bookMentorship = async (mentorId, scheduledTime) => {
  const response = await axios.post(`${API_URL}/mentorship/book`, {
    mentor_id: mentorId,
    scheduled_time: scheduledTime
  }, { withCredentials: true });
  return response.data;
};

export const completeMentorship = async (sessionId) => {
  const response = await axios.post(`${API_URL}/mentorship/complete/${sessionId}`, {}, { withCredentials: true });
  return response.data;
};

export const cancelMentorship = async (sessionId) => {
  const response = await axios.post(`${API_URL}/mentorship/cancel/${sessionId}`, {}, { withCredentials: true });
  return response.data;
};

export const getMentorshipHistory = async () => {
  const response = await axios.get(`${API_URL}/mentorship/history`, { withCredentials: true });
  return response.data;
};

export const getUpcomingMentorships = async () => {
const response = await axios.get(`${API_URL}/mentorship/mentor_requests`, { withCredentials: true });
return response.data.upcoming_sessions;
};

export const submitFeedback = async (sessionId, feedback) => {
  const response = await axios.post(`${API_URL}/mentorship/feedback/${sessionId}`, { feedback }, { withCredentials: true });
  return response.data;
};

// Post APIs
export const addPost = async (title, content) => {
  const response = await axios.post(`${API_URL}/post`, { title, content }, { withCredentials: true });
  return response;
};

export const getPosts = async () => {
  const response = await axios.get(`${API_URL}/posts`, { withCredentials: true });
  return response.data.posts;
};


export const getPostsByUser = async (id) => {
  const response = await axios.get(`${API_URL}/posts/${id}`, { withCredentials: true });
  return response.data.posts;
};

export const getPostsCurrentUser = async ()=>{
  return await getPostsByUser((await axios.get(`${API_URL}/ping`, { withCredentials: true })).data.id);
}


export const getPostById = async (postId) => {
  const response = await axios.get(`${API_URL}/posts/${postId}`, { withCredentials: true });
  return response.data;
};

export const deletePost = async (postId) => {
  const response = await axios.delete(`${API_URL}/posts/${postId}`, { withCredentials: true });
  return response.data;
};


export const vote = async (postId, vote_type) => {
  const response = await axios.post(`${API_URL}/posts/${postId}/vote`, { vote_type }, { withCredentials: true });
  return response.data.message;
};

export const comment = async (postId, comment_text) => {
  const response = await axios.post(`${API_URL}/posts/${postId}/comment`, { comment_text }, { withCredentials: true });
  return response.data;
};

// Scholarships and Internships
export const getScholarships = async () => {
  const response = await axios.get(`${API_URL}/scholarships`, { withCredentials: true });
  return response.data;
};

export const postScholarship = async (title, description, amount, requirements, application_link, deadline) => {
  const response = await axios.post(`${API_URL}/scholarships`, {
    title,
    description,
    amount,
    requirements,
    application_link,
    deadline,
  }, { withCredentials: true });
  return response.data;
};

export const getInternships = async () => {
  const response = await axios.get(`${API_URL}/internships`, { withCredentials: true });
  return response.data;
};

export const postInternship = async (title, description, requirements, application_link, deadline) => {
  const response = await axios.post(`${API_URL}/internships`, {
    title,
    description,
    requirements,
    application_link,
    deadline,
  }, { withCredentials: true });
  return response.data;
};

export const updateMentorshipSession = async (sessionId, updateType) => {
  const response = await axios.post(`${API_URL}/mentorship/update/${sessionId}`, {
    type: updateType
  }, { withCredentials: true });
  return response.data;
};

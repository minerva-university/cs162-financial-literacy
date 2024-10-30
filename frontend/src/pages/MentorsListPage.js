import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getAvailableMentors } from '../services/api';

const MentorsListPage = () => {
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch mentors when the component loads
    async function fetchMentors() {
      try {
        const availableMentors = await getAvailableMentors();
        setMentors(availableMentors.mentors); // Ensure it uses the right data structure
      } catch (error) {
        console.error("Failed to fetch mentors", error);
      } finally {
        setLoading(false);
      }
    }
    fetchMentors();
  }, []);

  if (loading) return <div>Loading mentors...</div>;

  if (mentors.length === 0) {
    return <div>No mentors are available for mentorship at the moment.</div>;
  }

  return (
    <div>
      <h1>Available Mentors</h1>
      <ul>
        {mentors.map((mentor) => (
          <li key={mentor.id}>
            <Link to={`/user/${mentor.id}`}>
              {mentor.name} - Mentorship Available
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MentorsListPage;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getAvailableMentors } from '../services/api';

const MentorsListPage = () => {
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');

  useEffect(() => {
    fetchMentors();
  }, [company, role]);

  const fetchMentors = async () => {
    setLoading(true);
    try {
      const availableMentors = await getAvailableMentors(company, role);
      setMentors(availableMentors.mentors);
    } catch (error) {
      console.error("Failed to fetch mentors", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading mentors...</div>;

  return (
    <div>
      <h1>Available Mentors</h1>
      <div>
        <input
          type="text"
          placeholder="Filter by company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
        />
        <input
          type="text"
          placeholder="Filter by role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />
      </div>
      {mentors.length === 0 ? (
        <div>No mentors are available for mentorship at the moment.</div>
      ) : (
        <ul>
          {mentors.map((mentor) => (
            <li key={mentor.id}>
              <Link to={`/user/${mentor.id}`}>
                {mentor.name} - Mentorship Available
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorsListPage;

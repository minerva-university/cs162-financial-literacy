import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getAvailableMentors, bookMentorship } from "../services/api";
import "../styles/MentorsList.css";

const MentorsListPage = () => {
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMentors() {
      try {
        const response = await getAvailableMentors();
        setMentors(response.mentors);
      } catch (error) {
        console.error("Failed to fetch mentors:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchMentors();
  }, []);

  const handleRequestMentorship = async (mentorId) => {
    try {
      const scheduledTime = prompt("Enter a scheduled time (YYYY-MM-DD HH:MM):");
      if (!scheduledTime) return;

      const response = await bookMentorship(mentorId, scheduledTime);
      alert(`Mentorship session booked! Credits left: ${response.credits}`);
    } catch (error) {
      alert("Failed to request mentorship. Please try again.");
      console.error("Mentorship request error:", error);
    }
  };

  if (loading) return <div>Loading mentors...</div>;

  if (mentors.length === 0) {
    return <div>No mentors are available for mentorship at the moment.</div>;
  }

  return (
    <div className="mentors-page">
      <h1>Available Mentors</h1>
      <ul className="mentors-list">
        {mentors.map((mentor) => (
          <li key={mentor.id} className="mentor-card">
            <Link to={`/user/${mentor.id}`}>
              <h3>{mentor.name}</h3>
              <p>{mentor.bio}</p>
            </Link>
            <button onClick={() => handleRequestMentorship(mentor.id)}>
              Request Mentorship
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MentorsListPage;

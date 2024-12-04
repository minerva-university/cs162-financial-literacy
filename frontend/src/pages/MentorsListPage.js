import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  getAvailableMentors,
  bookMentorship,
  getUpcomingMentorships,
  getMentorshipHistory,
  submitFeedback,
} from "../services/api";
import "../styles/MentorsList.css";

const MentorsListPage = () => {
  const [mentors, setMentors] = useState([]);
  const [upcomingSessions, setUpcomingSessions] = useState([]);
  const [mentorshipHistory, setMentorshipHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch available mentors
        const mentorsResponse = await getAvailableMentors();
        setMentors(mentorsResponse.mentors);

        // Fetch upcoming sessions
        const upcomingResponse = await getUpcomingMentorships();
        setUpcomingSessions(upcomingResponse.upcoming_sessions);

        // Fetch mentorship history
        const historyResponse = await getMentorshipHistory();
        setMentorshipHistory(historyResponse.mentorship_history);
      } catch (error) {
        console.error("Error fetching mentorship data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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

  const handleSubmitFeedback = async (sessionId) => {
    const feedback = prompt("Enter your feedback for this session:");
    if (!feedback) return;

    setFeedbackLoading(true);
    try {
      const response = await submitFeedback(sessionId, feedback);
      alert(response.message);
    } catch (error) {
      alert("Failed to submit feedback. Please try again.");
      console.error("Feedback submission error:", error);
    } finally {
      setFeedbackLoading(false);
    }
  };

  if (loading) return <div>Loading mentorship data...</div>;

  return (
    <div className="mentors-page">
      <h1>Find Mentors</h1>

      {/* Available Mentors Section */}
      <section className="mentors-section">
        <h2>Available Mentors</h2>
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
      </section>

      {/* Upcoming Sessions Section */}
      <section className="sessions-section">
        <h2>Upcoming Mentorship Sessions</h2>
        {upcomingSessions.length > 0 ? (
          <ul className="sessions-list">
            {upcomingSessions.map((session) => (
              <li key={session.session_id}>
                <p>
                  Mentor: {session.mentor.name} | Scheduled Time:{" "}
                  {session.scheduled_time}
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No upcoming sessions scheduled.</p>
        )}
      </section>

      {/* Mentorship History Section */}
      <section className="history-section">
        <h2>Mentorship History</h2>
        {mentorshipHistory.length > 0 ? (
          <ul className="history-list">
            {mentorshipHistory.map((history) => (
              <li key={history.session_id}>
                <p>
                  Mentor: {history.mentor.name} | Status: {history.status} | Date:{" "}
                  {history.scheduled_time}
                </p>
                {history.status === "completed" && (
                  <button
                    onClick={() => handleSubmitFeedback(history.session_id)}
                    disabled={feedbackLoading}
                  >
                    {feedbackLoading ? "Submitting..." : "Submit Feedback"}
                  </button>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p>No mentorship history found.</p>
        )}
      </section>
    </div>
  );
};

export default MentorsListPage;

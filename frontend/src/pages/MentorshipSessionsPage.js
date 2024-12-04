import React, { useState, useEffect } from "react";
import { cancelMentorship, getUpcomingMentorships } from "../services/api";
import "../styles/SessionsPage.css";

const MentorshipSessionsPage = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSessions() {
      try {
        const response = await getUpcomingMentorships();
        setSessions(response.upcoming_sessions);
      } catch (error) {
        console.error("Failed to fetch sessions:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchSessions();
  }, []);

  const handleCancelSession = async (sessionId) => {
    try {
      await cancelMentorship(sessionId);
      alert("Session canceled successfully!");
      setSessions(sessions.filter((session) => session.session_id !== sessionId));
    } catch (error) {
      console.error("Failed to cancel session:", error);
      alert("Failed to cancel session.");
    }
  };

  if (loading) return <div>Loading sessions...</div>;

  return (
    <div className="sessions-page">
      <h1>Upcoming Mentorship Sessions</h1>
      {sessions.length === 0 ? (
        <p>No upcoming sessions found.</p>
      ) : (
        <ul className="sessions-list">
          {sessions.map((session) => (
            <li key={session.session_id} className="session-card">
              <p><strong>Mentor:</strong> {session.mentor.name || "Unknown"}</p>
              <p><strong>Mentee:</strong> {session.mentee.name || "Unknown"}</p>
              <p><strong>Scheduled Time:</strong> {session.scheduled_time}</p>
              <button onClick={() => handleCancelSession(session.session_id)}>
                Cancel Session
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorshipSessionsPage;

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
    <div className="sessions-page p-4">
      <h1 className="text-2xl font-bold mb-4">Upcoming Mentorship Sessions</h1>
      {sessions.length === 0 ? (
        <p className="text-gray-500">No upcoming sessions found.</p>
      ) : (
        <ul className="space-y-4">
          {sessions.map((session) => (
            <li key={session.session_id} className="bg-white p-4 rounded-lg shadow-md">
              <p><strong>Mentor:</strong> {session.mentor.name || "Unknown"}</p>
              <p><strong>Mentee:</strong> {session.mentee.name || "Unknown"}</p>
              <p><strong>Scheduled Time:</strong> {new Date(session.scheduled_time).toLocaleString()}</p>
              {session.event_id && (
                <p>
                  <strong>Google Calendar:</strong>{" "}
                  <a
                    href={`https://calendar.google.com/calendar/u/0/r/eventedit/${session.event_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View Event
                  </a>
                </p>
              )}
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

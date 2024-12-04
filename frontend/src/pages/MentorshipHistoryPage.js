import React, { useState, useEffect } from "react";
import { getMentorshipHistory } from "../services/api";
import "../styles/HistoryPage.css";

const MentorshipHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const response = await getMentorshipHistory();
        setHistory(response.mentorship_history);
      } catch (error) {
        console.error("Failed to fetch history:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, []);

  if (loading) return <div>Loading history...</div>;

  return (
    <div className="history-page">
      <h1>Mentorship History</h1>
      {history.length === 0 ? (
        <p>No mentorship history found.</p>
      ) : (
        <ul className="history-list">
          {history.map((session) => (
            <li key={session.session_id} className="history-card">
              <p><strong>Mentor:</strong> {session.mentor.name || "Unknown"}</p>
              <p><strong>Mentee:</strong> {session.mentee.name || "Unknown"}</p>
              <p><strong>Scheduled Time:</strong> {session.scheduled_time}</p>
              <p><strong>Status:</strong> {session.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorshipHistoryPage;

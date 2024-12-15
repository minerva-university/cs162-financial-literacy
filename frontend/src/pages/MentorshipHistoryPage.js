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
    <div className="history-page p-4">
      <h1 className="text-2xl font-bold mb-4">Mentorship History</h1>
      {history.length === 0 ? (
        <p className="text-gray-500">No mentorship history found.</p>
      ) : (
        <ul className="space-y-4">
          {history.map((session) => (
            <li key={session.session_id} className="bg-white p-4 rounded-lg shadow-md">
              <p><strong>Mentor:</strong> {session.mentor.name || "Unknown"}</p>
              <p><strong>Mentee:</strong> {session.mentee.name || "Unknown"}</p>
              <p><strong>Scheduled Time:</strong> {new Date(session.scheduled_time).toLocaleString()}</p>
              <p><strong>Status:</strong> {session.status}</p>
              {session.event_id && (
                <p>
                  <strong>Google Calendar Event:</strong>{" "}
                  <a
                    href={`https://calendar.google.com/calendar/u/0/r/eventedit/${session.event_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline"
                  >
                    View in Calendar
                  </a>
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorshipHistoryPage;

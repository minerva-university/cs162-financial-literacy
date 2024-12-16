import React, { useState, useEffect } from 'react';
import { getUpcomingMenteeRequests } from '../services/api';

const MentorshipUpcoming = () => {
  const [upcomingSessions, setUpcomingSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchUpcomingSessions() {
      try {
        const sessions = await getUpcomingMenteeRequests();
        sessions.sort((a, b) => new Date(a.scheduled_time) - new Date(b.scheduled_time));
        setUpcomingSessions(sessions);
      } catch (error) {
        console.error('Failed to fetch upcoming sessions:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchUpcomingSessions();
  }, []);

  if (loading) return <div>Loading upcoming sessions...</div>;

  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled':
        return 'bg-green-100';
      case 'pending':
        return 'bg-yellow-100';
      case 'canceled':
        return 'bg-red-100';
      default:
        return 'bg-gray-100';
    }
  };

  return (
    <div className="upcoming-sessions-page p-4">
      <h1 className="text-2xl font-bold mb-4">My Requested Mentorship Sessions</h1>
      {upcomingSessions.length === 0 ? (
        <p className="text-gray-500">No upcoming sessions found.</p>
      ) : (
        <ul className="space-y-4">
          {upcomingSessions.map((session) => (
            <li key={session.session_id} className={`p-4 rounded-lg shadow-md ${getStatusColor(session.status)}`}>
              <p><strong>Mentor:</strong> {session.mentor.name || "Unknown"}</p>
              <p><strong>Scheduled Time:</strong> {new Date(session.scheduled_time).toLocaleString()}</p>
              <p><strong>Status:</strong> {session.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorshipUpcoming;

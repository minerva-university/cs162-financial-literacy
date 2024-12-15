import React, { useState, useEffect } from 'react';
import { getUpcomingMentorships } from '../services/api';

const MentorshipRequest = () => {
  const [receivedRequests, setReceivedRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReceivedRequests = async () => {
      try {
        const response = await getUpcomingMentorships();
        
        setReceivedRequests(response);
      } catch (error) {
        console.error("Failed to fetch received requests:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchReceivedRequests();
  }, []);

  if (loading) return <div>Loading received requests...</div>;

  return (
    <div className="received-requests">
      <h2>Received Mentorship Requests</h2>
      {receivedRequests.length === 0 ? (
        <p>No received requests found.</p>
      ) : (
        <ul>
          {receivedRequests.map((request) => (
            <li key={request.session_id}>
              From: {request.mentee.name} - {new Date(request.scheduled_time).toLocaleString()}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorshipRequest;

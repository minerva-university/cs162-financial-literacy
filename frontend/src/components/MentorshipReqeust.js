import React, { useState, useEffect } from 'react';
import { getUpcomingMentorships, updateMentorshipSession } from '../services/api';

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

  const handleAccept = async (sessionId) => {
    try {
      await updateMentorshipSession(sessionId, 'scheduled');
      alert(`Accepted request with session ID: ${sessionId}`);
      setReceivedRequests(receivedRequests.map(request =>
        request.session_id === sessionId ? { ...request, status: 'scheduled' } : request
      ));
    } catch (error) {
      console.error(`Failed to accept request with session ID: ${sessionId}`, error);
      alert('Failed to accept the request. Please try again.');
    }
  };

  const handleReject = async (sessionId) => {
    try {
      await updateMentorshipSession(sessionId, 'canceled');
      alert(`Rejected request with session ID: ${sessionId}`);
      setReceivedRequests(receivedRequests.map(request =>
        request.session_id === sessionId ? { ...request, status: 'canceled' } : request
      ));
    } catch (error) {
      console.error(`Failed to reject request with session ID: ${sessionId}`, error);
      alert('Failed to reject the request. Please try again.');
    }
  };

  if (loading) return <div>Loading received requests...</div>;

  return (
    <div className="received-requests p-4">
      <h2 className="text-2xl font-bold mb-4">Received Mentorship Requests</h2>
      {receivedRequests.length === 0 ? (
        <p className="text-gray-500">No received requests found.</p>
      ) : (
        <ul className="space-y-4">
          {receivedRequests.map((request) => (
            <li key={request.session_id}>
              From: {request.mentee.name} - {new Date(request.scheduled_time).toLocaleString()}
              {request.status === 'pending' && (
                <>
                  <button onClick={() => handleAccept(request.session_id)}>Accept</button>
                  <button onClick={() => handleReject(request.session_id)}>Reject</button>
                </>
              )||<div>{request.status}</div>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorshipRequest;

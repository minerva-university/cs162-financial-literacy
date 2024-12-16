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

  if (loading) return <div className="text-center text-gray-500">Loading received requests...</div>;

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Received Mentorship Requests</h2>
      {receivedRequests.length === 0 ? (
        <p className="text-gray-500">No received requests found.</p>
      ) : (
        <ul className="space-y-4">
          {receivedRequests.map((request) => (
            <li key={request.session_id} className="bg-gray-100 p-4 rounded-lg shadow-sm">
              <p className="font-semibold">From: {request.mentee.name}</p>
              <p className="text-sm text-gray-600">{new Date(request.scheduled_time).toLocaleString()}</p>
              {request.status === 'pending' ? (
                <div className="flex space-x-2 mt-2">
                  <button onClick={() => handleAccept(request.session_id)} className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Accept</button>
                  <button onClick={() => handleReject(request.session_id)} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">Reject</button>
                </div>
              ) : (
                <div className="text-sm text-gray-500">{request.status}</div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MentorshipRequest;

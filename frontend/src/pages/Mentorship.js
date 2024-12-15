import React, { useEffect, useState } from 'react';
import {
    getUpcomingMentorships,
    bookMentorship,
    cancelMentorship,
    getMentorshipHistory,
    submitFeedback,
} from '../services/api';
import CalendarView from '../components/CalendarView';

function Mentorship() {
    const [upcomingSessions, setUpcomingSessions] = useState([]);
    const [history, setHistory] = useState([]);
    const [mentorId, setMentorId] = useState('');
    const [scheduledTime, setScheduledTime] = useState('');
    const [feedback, setFeedback] = useState('');
    const [sessionId, setSessionId] = useState('');
    const [events, setEvents] = useState([]);

    // Fetch upcoming mentorships
    useEffect(() => {
        async function fetchUpcoming() {
            try {
                const data = await getUpcomingMentorships();
                setUpcomingSessions(data.upcoming_sessions || []);
                const calendarEvents = data.upcoming_sessions.map(session => ({
                    title: `Mentorship with ${session.mentor.name}`,
                    start: new Date(session.scheduled_time),
                    end: new Date(new Date(session.scheduled_time).getTime() + 60 * 60 * 1000), // 1 hour duration
                }));
                setEvents(calendarEvents);
            } catch (error) {
                console.error('Error fetching upcoming mentorships:', error);
            }
        }
        fetchUpcoming();
    }, []);

    // Fetch mentorship history
    useEffect(() => {
        async function fetchHistory() {
            try {
                const data = await getMentorshipHistory();
                setHistory(data.mentorship_history || []);
            } catch (error) {
                console.error('Error fetching mentorship history:', error);
            }
        }
        fetchHistory();
    }, []);

    // Handle booking a mentorship session
    const handleBook = async () => {
        if (!mentorId || !scheduledTime) {
            alert('Please provide a mentor ID and scheduled time.');
            return;
        }
        try {
            const response = await bookMentorship(mentorId, scheduledTime);
            alert('Mentorship booked successfully!');
            // Update the events and upcoming sessions
            const newEvent = {
                title: `Mentorship with ${response.mentor.name}`,
                start: new Date(response.scheduled_time),
                end: new Date(new Date(response.scheduled_time).getTime() + 60 * 60 * 1000),
            };
            setEvents([...events, newEvent]);
            setUpcomingSessions([...upcomingSessions, response]);
        } catch (error) {
            console.error('Error booking mentorship:', error);
            alert('Error booking mentorship.');
        }
    };

    // Cancel a mentorship session
    const handleCancel = async (id) => {
        try {
            await cancelMentorship(id);
            alert('Mentorship canceled successfully!');
            setUpcomingSessions(upcomingSessions.filter((session) => session.session_id !== id));
        } catch (error) {
            console.error('Error canceling mentorship:', error);
            alert('Error canceling mentorship.');
        }
    };

    // Submit feedback
    const handleFeedback = async () => {
        if (!sessionId || !feedback) {
            alert('Please provide session ID and feedback.');
            return;
        }
        try {
            await submitFeedback(sessionId, feedback);
            alert('Feedback submitted successfully!');
            setFeedback('');
            setSessionId('');
        } catch (error) {
            console.error('Error submitting feedback:', error);
            alert('Error submitting feedback.');
        }
    };

    return (
        <div className="container p-4">
            <h1 className="text-2xl font-bold mb-4">Mentorship</h1>
            <CalendarView events={events} />
            <div className="booking-section mb-4">
                <h2 className="text-xl font-semibold mb-2">Book Mentorship</h2>
                <input
                    type="text"
                    placeholder="Mentor ID"
                    value={mentorId}
                    onChange={(e) => setMentorId(e.target.value)}
                />
                <input
                    type="datetime-local"
                    value={scheduledTime}
                    onChange={(e) => setScheduledTime(e.target.value)}
                />
                <button onClick={handleBook}>Book Session</button>
            </div>

            <div className="upcoming-section mb-4">
                <h2 className="text-xl font-semibold mb-2">Upcoming Sessions</h2>
                <ul>
                    {upcomingSessions.map((session) => (
                        <li key={session.session_id}>
                            {session.mentor.name} - {new Date(session.scheduled_time).toLocaleString()}
                            <button onClick={() => handleCancel(session.session_id)}>Cancel</button>
                        </li>
                    ))}
                </ul>
            </div>

            <div className="history-section mb-4">
                <h2 className="text-xl font-semibold mb-2">Mentorship History</h2>
                <ul>
                    {history.map((session) => (
                        <li key={session.session_id}>
                            {session.mentor.name} - {session.status}
                        </li>
                    ))}
                </ul>
            </div>

            <div className="feedback-section mb-4">
                <h2 className="text-xl font-semibold mb-2">Submit Feedback</h2>
                <input
                    type="text"
                    placeholder="Session ID"
                    value={sessionId}
                    onChange={(e) => setSessionId(e.target.value)}
                />
                <textarea
                    placeholder="Feedback"
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                />
                <button onClick={handleFeedback}>Submit Feedback</button>
            </div>
        </div>
    );
}

export default Mentorship;

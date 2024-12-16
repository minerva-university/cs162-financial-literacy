import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {
  getAvailableMentors,
  bookMentorship,
} from "../services/api";
import "../styles/MentorsList.css";
import { useMentorship } from '../pages/MentorshipContext';

const MentorsListPage = () => {
  const [mentors, setMentors] = useState([]);
  const [selectedMentor, setSelectedMentor] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate(); // For navigation between pages
  const { addCheckedUser } = useMentorship();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const mentorsResponse = await getAvailableMentors();
        console.log("Mentors Response:", mentorsResponse); // Add this line
        setMentors(mentorsResponse.mentors);
      } catch (error) {
        console.error("Error fetching mentors:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleRequestMentorship = async () => {
    if (!selectedMentor || !selectedDate) {
      alert("Please select a mentor and a valid date/time.");
      return;
    }

    const scheduledTime = selectedDate.toISOString();

    try {
      const response = await bookMentorship(selectedMentor, scheduledTime);
      alert(`Mentorship session booked! Credits left: ${response.credits}`);
      setSelectedMentor(null);
      setSelectedDate(null);
    } catch (error) {
      alert("Failed to request mentorship. Please try again.");
      console.error("Mentorship request error:", error);
    }
  };

  if (loading) return <div>Loading mentorship data...</div>;

  return (
    <div className="mentors-page p-4">
      <h1 className="text-2xl font-bold mb-4">Find Mentors</h1>

      {/* Navigation Buttons */}
      <div className="navigation-buttons flex justify-between mb-4">
        <button onClick={() => navigate("/mentorship/upcoming")}>
          View Upcoming Mentorships
        </button>
        <button onClick={() => navigate("/mentorship/history")}>
          View Mentorship History
        </button>
      </div>

      <section className="mentors-section">
        <h2 className="text-xl font-bold mb-4">Available Mentors</h2>
        <ul className="mentors-list">
          {mentors.map((mentor) => (
            <li key={mentor.id} className="mentor-card">
              <Link to={`/user/${mentor.id}`}>
                <h3 className="text-lg font-semibold">{mentor.name}</h3>
                <p className="text-gray-700">{mentor.bio}</p>
              </Link>
              {mentor.calendar_url && (
                <p>
                  <strong>Google Calendar:</strong>{" "}
                  <a
                    href={mentor.calendar_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={() => addCheckedUser(mentor.id)}
                  >
                    View Availability
                  </a>
                </p>
              )}
              <button onClick={() => setSelectedMentor(mentor.id)}>
                Request Mentorship
              </button>
            </li>
          ))}
        </ul>
      </section>

      {selectedMentor && (
        <div className="datepicker-modal">
          <h2 className="text-xl font-bold mb-4">Select Date and Time</h2>
          <DatePicker
            selected={selectedDate}
            onChange={(date) => setSelectedDate(date)}
            showTimeSelect
            timeFormat="HH:mm"
            timeIntervals={15}
            dateFormat="MMMM d, yyyy h:mm aa"
            minDate={new Date()}
            className="border p-2 rounded w-full"
            popperPlacement="auto"
            popperModifiers={{
              preventOverflow: {
                enabled: true,
                boundariesElement: 'viewport',
              },
            }}
          />
          <button onClick={handleRequestMentorship}>Confirm</button>
          <button onClick={() => setSelectedMentor(null)}>Cancel</button>
        </div>
      )}
    </div>
  );
};

export default MentorsListPage;

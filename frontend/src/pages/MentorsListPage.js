import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { getAvailableMentors, bookMentorship } from "../services/api";
import "../styles/MentorsList.css";
import { useMentorship } from "../pages/MentorshipContext";

const MentorsListPage = () => {
  const [mentors, setMentors] = useState([]);
  const [selectedMentor, setSelectedMentor] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();
  const { addCheckedUser } = useMentorship();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const mentorsResponse = await getAvailableMentors();
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

  if (loading) return <div className="loading">Loading mentorship data...</div>;

  return (
    <div className="mentors-page p-4">
      <h1 className="text-2xl font-bold mb-4">Find Your Mentor</h1>

      {/* Navigation Buttons */}
      <div className="navigation-buttons flex justify-between">
        <button
          onClick={() => navigate("/mentorship/upcoming")}
          className="nav-btn"
        >
          View Upcoming Mentorships
        </button>
        <button
          onClick={() => navigate("/mentorship/history")}
          className="nav-btn"
        >
          View Mentorship History
        </button>
      </div>

      {/* Available Mentors Section */}
      <section className="mentors-section mt-4">
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
                  <strong>Availability:</strong>{" "}
                  <a
                    href={mentor.calendar_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="calendar-link"
                    onClick={() => addCheckedUser(mentor.id)}
                  >
                    View Calendar
                  </a>
                </p>
              )}
              <button
                className="mentor-request-btn"
                onClick={() => setSelectedMentor(mentor.id)}
              >
                Request Mentorship
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* Date Picker Modal */}
      {selectedMentor && (
        <div className="datepicker-modal">
          <div className="modal-content">
            <h2 className="text-xl font-bold mb-4">Select Date and Time</h2>
            <DatePicker
              selected={selectedDate}
              onChange={(date) => setSelectedDate(date)}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              dateFormat="MMMM d, yyyy h:mm aa"
              minDate={new Date()}
              className="datepicker"
            />
            <div className="modal-actions">
              <button
                onClick={handleRequestMentorship}
                className="modal-btn confirm"
              >
                Confirm
              </button>
              <button
                onClick={() => setSelectedMentor(null)}
                className="modal-btn cancel"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MentorsListPage;

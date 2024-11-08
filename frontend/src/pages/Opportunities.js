import React, { useState, useEffect } from 'react';
import { getScholarships, getInternships } from '../services/api';

const Opportunities = () => {
  const [scholarships, setScholarships] = useState([]);
  const [internships, setInternships] = useState([]);

  useEffect(() => {
    const fetchOpportunities = async () => {
      try {
        const scholarshipData = await getScholarships();
        setScholarships(scholarshipData);
        const internshipData = await getInternships();
        setInternships(internshipData);
      } catch (error) {
        console.error("Failed to fetch opportunities", error);
      }
    };
    fetchOpportunities();
  }, []);

  return (
    <div>
      <h2>Scholarships</h2>
      {scholarships.length > 0 ? (
        scholarships.map((scholarship) => (
          <div key={scholarship.id}>
            <h3>{scholarship.title}</h3>
            <p>{scholarship.description}</p>
            <a href={scholarship.application_link} target="_blank" rel="noopener noreferrer">Apply</a>
          </div>
        ))
      ) : (
        <p>No scholarships available at the moment.</p>
      )}
      <h2>Internships</h2>
      {internships.length > 0 ? (
        internships.map((internship) => (
          <div key={internship.id}>
            <h3>{internship.title}</h3>
            <p>{internship.description}</p>
            <a href={internship.application_link} target="_blank" rel="noopener noreferrer">Apply</a>
          </div>
        ))
      ) : (
        <p>No internships available at the moment.</p>
      )}
    </div>
  );
};

export default Opportunities;

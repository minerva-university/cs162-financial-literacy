import React, { useState, useEffect } from 'react';
import { getInternships } from '../services/api';

const InternshipsPage = () => {
  const [internships, setInternships] = useState([]);

  useEffect(() => {
    const fetchInternships = async () => {
      try {
        const internshipData = await getInternships();
        setInternships(internshipData);
      } catch (error) {
        console.error("Failed to fetch internships", error);
      }
    };
    fetchInternships();
  }, []);

  return (
    <div>
      <h1>Internships</h1>
      {internships.length > 0 ? (
        internships.map((internship) => (
          <div key={internship.id}>
            <h3>{internship.title}</h3>
            <p>{internship.description}</p>
            <a href={internship.application_link} target="_blank" rel="noopener noreferrer">
              Apply
            </a>
          </div>
        ))
      ) : (
        <p>No internships available at the moment.</p>
      )}
    </div>
  );
};

export default InternshipsPage;
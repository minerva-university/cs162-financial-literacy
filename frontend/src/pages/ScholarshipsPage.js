import React, { useState, useEffect } from 'react';
import { getScholarships } from '../services/api';

const ScholarshipsPage = () => {
  const [scholarships, setScholarships] = useState([]);

  useEffect(() => {
    const fetchScholarships = async () => {
      try {
        const scholarshipData = await getScholarships();
        setScholarships(scholarshipData);
      } catch (error) {
        console.error("Failed to fetch scholarships", error);
      }
    };
    fetchScholarships();
  }, []);

  return (
    <div>
      <h1>Scholarships</h1>
      {scholarships.length > 0 ? (
        scholarships.map((scholarship) => (
          <div key={scholarship.id}>
            <h3>{scholarship.title}</h3>
            <p>{scholarship.description}</p>
            <a href={scholarship.application_link} target="_blank" rel="noopener noreferrer">
              Apply
            </a>
          </div>
        ))
      ) : (
        <p>No scholarships available at the moment.</p>
      )}
    </div>
  );
};

export default ScholarshipsPage;
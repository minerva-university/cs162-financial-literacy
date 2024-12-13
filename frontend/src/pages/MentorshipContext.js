import React, { createContext, useState, useContext } from 'react';

const MentorshipContext = createContext();

export const useMentorship = () => useContext(MentorshipContext);

export const MentorshipProvider = ({ children }) => {
  const [checkedUsers, setCheckedUsers] = useState([]);

  const addCheckedUser = (userId) => {
    setCheckedUsers((prev) => [...new Set([...prev, userId])]);
  };

  return (
    <MentorshipContext.Provider value={{ checkedUsers, addCheckedUser }}>
      {children}
    </MentorshipContext.Provider>
  );
};

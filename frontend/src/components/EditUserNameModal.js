import React, { useState } from 'react';
import { updateUserName } from '../services/api';

const EditUserNameModal = ({ userData, setUserData, closeModal }) => {
  const [newName, setNewName] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const result = await updateUserName(newName);
    if (result.success) {
      setUserData({ ...userData, name: newName });
      closeModal();
    }
  };

  return (
    <div className="modal">
      <form onSubmit={handleSubmit}>
        <label>New User Name:</label>
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <button type="submit">Save</button>
        <button type="button" onClick={closeModal}>Cancel</button>
      </form>
    </div>
  );
};

export default EditUserNameModal;

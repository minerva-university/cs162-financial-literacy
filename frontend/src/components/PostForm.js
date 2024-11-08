import React, { useState } from 'react';
import { addPost } from '../services/api';

const PostForm = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await addPost(title, content);
    if (result.success) {
      alert('Post added successfully!');
    } else {
      alert('Failed to add post.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
      <textarea placeholder="Content" value={content} onChange={(e) => setContent(e.target.value)} />
      <button type="submit">Post</button>
    </form>
  );
};

export default PostForm;

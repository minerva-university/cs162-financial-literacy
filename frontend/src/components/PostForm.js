import React, { useState } from 'react';
import { addPost } from '../services/api';
import Editor from 'react-simple-wysiwyg';
import { Link } from 'react-router-dom';



const PostForm = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await addPost(title, content);
    if (result.status == 201) {
      alert('Post added successfully!');
    } else {
      alert('Failed to add post.');
    }
  };

  return (
    <>
    <form onSubmit={handleSubmit} className="flex flex-col space-y-4 max-w-[600px] mx-auto p-10">
      <input
        type="text"
        placeholder="Title"
        value={title}
        required
        onChange={(e) => setTitle(e.target.value)}
        className="rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <div className="relative">
        <Editor
          aria-required
          id="my-editor"
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 h-48 resize-none"
        />
        <div className="absolute top-0 right-0 flex items-center mr-4">
          <button type="button" className="text-gray-500 hover:text-blue-500 mr-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"   

                strokeLinejoin="round"
                strokeWidth="2"
                d="M14.742   
 3.742L12 6.485l2.742 2.742M6 12c4.418 0 8 3.582 8 8s-3.582 8-8 8-8-3.582-8-8 3.582-8 8-8z"
              />
            </svg>
          </button>
          <button type="button" className="text-gray-500 hover:text-blue-500">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"   

                strokeLinejoin="round"
                strokeWidth="2"
                d="M17.257   
 14.742L12 21l-5.257-6.258M12 5l6 6v10h-12V5z"
              />
            </svg>
          </button>
        </div>
      </div>
      <button type="submit" className="bg-blue-500 text-white hover:bg-blue-700 font-bold py-2 rounded-lg">
        Post
      </button>
    </form>
    </>
  );
};

export default PostForm;

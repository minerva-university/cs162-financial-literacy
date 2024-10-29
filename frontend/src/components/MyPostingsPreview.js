import React from 'react';
import { Link } from 'react-router-dom';

const MyPostingsPreview = ({ postings }) => {
  return (
    <div>
      <h3>My Postings</h3>
      {postings.length === 0 ? (
        <p>No postings yet.</p>
      ) : (
        <ul>
          {postings.map((post) => (
            <li key={post.id}>
              <Link to={`/post/${post.id}`}>{post.title}</Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MyPostingsPreview;

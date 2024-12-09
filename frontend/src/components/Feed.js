import React, { useState, useEffect } from 'react';
import HTMLRenderer from 'react-html-renderer';
import { Link } from 'react-router-dom';
import '../styles/PostFeed.css';
import { deletePost } from '../services/api';

const PostFeed = ({posts, error, isLoading, deleteOption}) => {
  

  if (isLoading) {
    return <div className="loading-container">Loading posts...</div>;
  }

  if (error) {
    return <div className="error-container">Error fetching posts: {error.message}</div>;
  }

  async function deletePostHandler(id){
    const response = await deletePost(id);
    if (response.message == 'Post deleted successfully'){
      window.location.reload();
    } else {
      alert("An error happened")
    }
  }

  return (
    <div className="feed-container">
      {posts?.map((post) => (
        <div key={post.id} className="post-card">
          <Link to={`/post/${post.id}`} className="post-title-link">
            <h2 className="post-title">{post.title}</h2>
          </Link>
          <HTMLRenderer html={post.content} />
          <div className="post-meta">
            <p className="post-author">Author: {post.author}</p>
            <p className="post-date">Created At: {post.created_at}</p>
          </div>
          {deleteOption&&<button className='bg-red-600 p-1 rounded-2xl' onClick={deletePostHandler(post.id)}>
            X Delete Post
          </button>}
        </div>
      ))}
      <Link to="/post" className="write-post-button">
        + Write a Post!
      </Link>
    </div>
  );
};

export default PostFeed;

import React, { useState, useEffect } from 'react';
import HTMLRenderer from 'react-html-renderer';
import { Link } from 'react-router-dom';
import { getPosts } from '../services/api';
import '../styles/PostFeed.css';

const PostFeed = () => {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setPosts(await getPosts());
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (isLoading) {
    return <div className="loading-container">Loading posts...</div>;
  }

  if (error) {
    return <div className="error-container">Error fetching posts: {error.message}</div>;
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
        </div>
      ))}
      <Link to="/post" className="write-post-button">
        + Write a Post!
      </Link>
    </div>
  );
};

export default PostFeed;

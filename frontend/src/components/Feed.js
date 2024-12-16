import React, { useState, useEffect } from 'react';
import HTMLRenderer from 'react-html-renderer';
import { Link } from 'react-router-dom';
import '../styles/PostFeed.css';
import { deletePost, getPostsSortedByDate, getPostsSortedByVotes } from '../services/api';

const PostFeed = ({deleteOption, posts, type, setPosts}) => {
  
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const [sortBy, setSortBy] = useState('date'); // can be 'date' or 'votes'
  const [direction, setDirection] = useState('desc'); // can be 'asc' or 'desc'

  useEffect(() => {
    const fetchPosts = async () => {
      setIsLoading(true);
      setError(null);
      try {
        let fetchedPosts = [];
        if (sortBy === 'date') {
          fetchedPosts = await getPostsSortedByDate(direction);
        } else {
          fetchedPosts = await getPostsSortedByVotes(direction);
        }
        setPosts(fetchedPosts);
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, [sortBy, direction]);

  async function deletePostHandler(id) {
    const response = await deletePost(id);
    if (response.message === 'Post deleted successfully') {
      window.location.reload();
    } else {
      alert("An error happened");
    }
  }

  if (isLoading) {
    return <div className="loading-container">Loading posts...</div>;
  }

  if (error) {
    return <div className="error-container">Error fetching posts: {error.message}</div>;
  }

  return (
    <div className="feed-container">
      {type=="Global"&&<div className="sorting-controls" style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <label>
          Sort By: 
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} style={{ marginLeft: '0.5rem' }}>
            <option value="date">Date</option>
            <option value="votes">Votes</option>
          </select>
        </label>
        <label>
          Direction: 
          <select value={direction} onChange={(e) => setDirection(e.target.value)} style={{ marginLeft: '0.5rem' }}>
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </label>
      </div>}

      {posts?.map((post) => (
        <div key={post.id} className="post-card">
          <Link to={`/post/${post.id}`} className="post-title-link">
            <h2 className="post-title">{post.title}</h2>
          </Link>
          <HTMLRenderer html={post.content} />
          <div className="post-meta">
            <Link to={`/user/${post.author_id}`} className="post-title-link">
              <p className="post-author"> Author: {post.author}</p>
            </Link>
            <p className="post-date">Created At: {post.created_at}</p>
            {post.vote_count !== undefined && <p className="post-votes">Votes: {post.vote_count}</p>}
          </div>
          {deleteOption && <button className='bg-red-600 p-1 rounded-2xl' onClick={() => deletePostHandler(post.id)}>
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

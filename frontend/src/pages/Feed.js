import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HTMLRenderer from 'react-html-renderer'
import { Link } from 'react-router-dom';

const PostFeed = () => {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('/posts');
        setPosts(response.data.posts);
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading posts...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen">Error fetching posts: {error.message}</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-1 gap-4 max-w-[600px] mx-auto py-20">
      {posts.map((post) => (
        <div key={post.id} className="bg-white rounded-lg shadow-md p-4">
          <h2 className="text-xl font-bold mb-2">{post.title}</h2>
          <HTMLRenderer html={post.content}> </HTMLRenderer>
          <p className="text-gray-500 text-sm">Author: {post.author}</p>
          <p className="text-gray-400 text-sm">Created At: {post.created_at}</p>
          
        </div>
      ))}
    <Link to="/post">
      <button className='fixed right-10 bottom-10 rounded-lg bg-green-500 m-5 p-5'>
        + Write a post!
      </button>
    </Link>
    </div>
  );
};

export default PostFeed;
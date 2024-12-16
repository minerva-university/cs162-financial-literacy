import React, { useState, useEffect } from 'react';
import PostFeed from '../components/Feed';
import { getFollowingPosts, getPosts } from '../services/api';

function FeedPage() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [type, setType] = useState("Global");

  useEffect(() => {
    const fetchPosts = async () => {
      setIsLoading(true);
      setError(null);
      try {
        if (type === "Global") {
          setPosts(await getPosts());
        } else if (type === "Following") {
          setPosts(await getFollowingPosts());
        }
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, [type]); // Re-fetch posts whenever `type` changes

  return (
    <><div className='p-2'>
      <button
        className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75 mx-auto"
        onClick={() => setType(type === "Global" ? "Following" : "Global")}
      >
        Switch to {type === "Global" ? "Following" : "Global"} Feed
      </button>
      </div>
      <PostFeed posts={posts} setPosts={setPosts} error={error} isLoading={isLoading} deleteOption={false} type={type}/>
    </>
  );
}

export default FeedPage;

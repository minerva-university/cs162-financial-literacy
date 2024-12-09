import React, {useState, useEffect} from 'react'
import PostFeed from '../components/Feed';
import { getPosts } from '../services/api';

function FeedPage() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
    
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setPosts(await getPosts());
        console.log(posts)
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, []);
  return (
    <PostFeed posts={posts} error={error} isLoading={isLoading} deleteOption={false}/>
  )
}

export default FeedPage
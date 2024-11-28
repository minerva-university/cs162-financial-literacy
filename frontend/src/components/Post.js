import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { comment, getPostById, vote } from '../services/api';
import { Link, useParams } from 'react-router-dom';
import HTMLRenderer from 'react-html-renderer';
import { Editor, EditorProvider } from 'react-simple-wysiwyg';

const PostPage = () => {
  const { postId } = useParams();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [userVote, setUserVote] = useState(null)

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const post = await getPostById(postId);
        setPost(post);
        setComments(post.comments);
        console.log(post.comments)
        if (post.user_has_upvoted){
          setUserVote("upvote")
        } else if (post.user_has_downvoted){
          setUserVote("downvote")
        }
      } catch (error) {
        console.error(error);
      }
    };

    fetchPost();
  }, [postId]);

  const handleUpvote = async () => {
    try {
      const message = await vote(postId, 'upvote');
      if (message == "Vote updated successfully"){
        setPost((prevPost) => ({ ...prevPost, upvotes: prevPost.upvotes + 1, downvotes:prevPost.downvotes-1 }));
        setUserVote("upvote")
      } else if (message == "Vote added successfully"){
        setPost((prevPost) => ({ ...prevPost, upvotes: prevPost.upvotes + 1 }));
        setUserVote("upvote")
      } else {
        setPost((prevPost) => ({ ...prevPost, upvotes: prevPost.upvotes - 1 }));
        setUserVote("")
      }
      
    } catch (error) {
      console.error(error);
    }
  };

  const handleDownvote = async () => {
    try {
      const message = await vote(postId, 'downvote');
      if (message == "Vote updated successfully"){
        setPost((prevPost) => ({ ...prevPost, upvotes: prevPost.upvotes - 1, downvotes:prevPost.downvotes + 1 }));
        setUserVote("downvote")
      } else if (message == "Vote added successfully"){
        console.log("Added succsessfully")
        setPost((prevPost) => ({ ...prevPost, downvotes: prevPost.downvotes + 1 }));
        setUserVote("downvote")
      } else {
        setPost((prevPost) => ({ ...prevPost, downvotes: prevPost.downvotes - 1 }));
        setUserVote("")
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmitComment = async (e) => {
    e.preventDefault();
    try {
      const newCom =  (await comment(postId, newComment)).comment;
      console.log(newCom)
      setComments([...comments, { id: newCom.user_id, user:{name: newCom.name, id: newCom.user_id}, comment_text: newComment, created_at:newCom.created_at }]);
      setNewComment('');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="post-container border border-gray-300 rounded-lg shadow-sm p-4 max-w-[600px] mx-auto my-10">
      {post && (
        <>
          <div className="post-header border-b border-gray-200 pb-4">
            <h2 className="text-2xl font-semibold">{post.post.title}</h2>
            <p className="text-gray-500 text-sm">Author: {post.post.user.name}</p>
            <p className="text-gray-400 text-sm">Created At: {post.post.created_at}</p>
            <div className="m-3">
              <HTMLRenderer html={post.post.content}  />
            </div>
            
          </div>
          <div className="vote-section flex justify-between items-center pt-4">
            <button
              onClick={() => handleUpvote()}
              className={`text-white font-bold py-2 px-4 rounded-md ${
                userVote === 'upvote' ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              Upvote ({post.upvotes})
            </button>
            <button
              onClick={() => handleDownvote()}
              className={`text-white font-bold py-2 px-4 rounded-md ${
                userVote === 'downvote' ? 'bg-red-500' : 'bg-gray-300'
              }`}
            >
              Downvote ({post.downvotes})
            </button>
          </div>
          <div className="comments-section border-t border-gray-200 pt-4">
            <h3>Comments</h3>
            {comments.length > 0 ? (
              comments.map((comment) => (
                <div key={comment.comment_id} className="comment mb-4 border-2 rounded-md p-2">
                  <h4 className=' text-xl'>{comment.user.name}</h4>
                  <p className="text-gray-400 text-sm">{comment.created_at}</p>
                  <HTMLRenderer html={comment.comment_text} />
                </div>
              ))
            ) : (
              <p>No comments</p>
            )}
          </div>
          <div className="comment-form mt-4">
            <form onSubmit={handleSubmitComment}>
              <EditorProvider>
                <Editor
                  aria-required
                  id="my-editor"
                  placeholder="Comment"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  className="rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 h-48 resize-none"
                />
              </EditorProvider>
              
              <button type="submit" className="bg-blue-500 text-white font-bold py-2 px-4 rounded-md">
                Comment
              </button>
            </form>
          </div>
        </>
      )}
    <Link to="/feed">
      <button className='fixed left-10 bottom-10 rounded-lg bg-blue-500 m-5 p-5'>
        Go back to the feed
      </button>
    </Link>
    </div>
  );
};

export default PostPage;
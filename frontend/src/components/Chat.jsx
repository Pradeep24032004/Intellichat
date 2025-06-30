
import React, { useEffect, useState, useRef } from 'react';
import { postMessage, postAIMessage, getMessages, deleteMessage } from '../api.js';
import './Chat.css';

export default function Chat({ token: propToken, logout }) {
  const [messages, setMessages] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);
  const [isAIMode, setIsAIMode] = useState(false);
  const [isAILoading, setIsAILoading] = useState(false);

  const token = propToken || localStorage.getItem('token');

  // Map of username -> color
  const userColorMap = useRef({});

  // Function to generate dark color
  const getRandomDarkColor = () => {
    const h = Math.floor(Math.random() * 360);
    const s = 60 + Math.random() * 20;
    const l = 25 + Math.random() * 15;
    return `hsl(${h}, ${s}%, ${l}%)`;
  };

  // Get user color (generate if not exists)
  const getUserColor = (username) => {
    if (username === 'AI Assistant') {
      return '#4A90E2'; // Special color for AI
    }
    if (!userColorMap.current[username]) {
      userColorMap.current[username] = getRandomDarkColor();
    }
    return userColorMap.current[username];
  };

  // Get current user ID from token
  const getCurrentUserIdFromToken = () => {
    if (!token) return null;
    
    try {
      // Decode JWT token to get user info
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.sub; // This should be the email, we'll match it with messages
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  };

  const fetchMessages = async () => {
    try {
      const res = await getMessages(token);
      setMessages(res.data);
      
      // Get current user email from token
      const currentUserEmail = getCurrentUserIdFromToken();
      
      if (currentUserEmail && res.data.length > 0) {
        // Find the current user's message to get their user_id
        const currentUserMessage = res.data.find(msg => msg.email === currentUserEmail && !msg.is_ai);
        if (currentUserMessage) {
          console.log('Current User ID:', currentUserMessage.user_id);
          setCurrentUserId(currentUserMessage.user_id);
        } else {
          // If no messages from current user, we need to get user_id differently
          // For now, we'll set it when they send their first message
          console.log('No messages from current user yet');
        }
      }
    } catch (err) {
      console.error('Error fetching messages:', err);
      alert('Could not fetch messages');
    }
  };

  const handlePost = async (e) => {
    e.preventDefault();
    const { content } = e.target;
    
    if (!content.value.trim()) return;
    
    try {
      let response;
      
      if (isAIMode) {
        setIsAILoading(true);
        response = await postAIMessage(token, { content: content.value });
        setIsAILoading(false);
      } else {
        response = await postMessage(token, { content: content.value });
      }
      
      // Set current user ID from the response if not already set
      if (!currentUserId && response.data && response.data.user_id && !response.data.is_ai) {
        setCurrentUserId(response.data.user_id);
        console.log('Set current user ID from post response:', response.data.user_id);
      }
      
      content.value = '';
      fetchMessages();
    } catch (error) {
      console.error('Error posting message:', error);
      setIsAILoading(false);
      alert('Message failed');
    }
  };

  const handleDelete = async (msgUserId, msgId, isAI) => {
    // Allow deletion of own messages or AI messages that user requested
    if (!isAI && msgUserId !== currentUserId) {
      alert("You cannot delete this message.");
      return;
    }
    
    try {
      await deleteMessage(token, msgId);
      fetchMessages();
    } catch (err) {
      console.error('Error deleting message:', err);
      alert('Failed to delete message.');
    }
  };

  useEffect(() => {
    fetchMessages(); // initial fetch
    const interval = setInterval(fetchMessages, 3000); // fetch every 3 seconds
    return () => clearInterval(interval); // cleanup on unmount
  }, []);

  return (
    <div className="chat">
      <div className="chat-header">
        <h2 className="chat-room">Chat Room</h2>
        <div className="chat-mode-toggle">
          <button 
            className={`mode-btn ${!isAIMode ? 'active' : ''}`}
            onClick={() => setIsAIMode(false)}
          >
            💬 Chat
          </button>
          <button 
            className={`mode-btn ${isAIMode ? 'active' : ''}`}
            onClick={() => setIsAIMode(true)}
          >
            🤖 AI Chat
          </button>
        </div>
      </div>

      <div className="msgs">
        {messages.map((msg) => {
          const isOwnMessage = msg.user_id === currentUserId;
          const isAIMessage = msg.is_ai || msg.username === 'AI Assistant';

          return (
            <div
              key={msg.id}
              className={`msg ${isOwnMessage ? 'own-msg' : isAIMessage ? 'ai-msg' : 'other-msg'}`}
            >
              <div className="msg-content-wrapper">
                <p
                  className="usrname"
                  style={{ color: getUserColor(msg.username) }}
                >
                  {isAIMessage ? '🤖 ' + msg.username : msg.username}
                </p>
                <p className="msg-content">{msg.content}</p>
                <p className="dt">{new Date(msg.timestamp).toLocaleString()}</p>
              </div>
              {(isOwnMessage || (isAIMessage && currentUserId)) && (
                <button
                  onClick={() => handleDelete(msg.user_id, msg.id, isAIMessage)}
                  className="dlt-msg"
                >
                  Delete
                </button>
              )}
            </div>
          );
        })}
        {isAILoading && (
          <div className="msg ai-msg">
            <div className="msg-content-wrapper">
              <p className="usrname" style={{ color: '#4A90E2' }}>
                🤖 AI Assistant
              </p>
              <p className="msg-content typing-indicator">
                <span></span>
                <span></span>
                <span></span>
                Typing...
              </p>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handlePost} className="message-form">
        <input
          name="content"
          placeholder={isAIMode ? "Ask AI anything..." : "Type your message..."}
          className="input"
          required
          disabled={isAILoading}
        />
        <button 
          type="submit" 
          className={`btn ${isAIMode ? 'ai-btn' : ''}`}
          disabled={isAILoading}
        >
          {isAILoading ? '🤖...' : isAIMode ? '🤖 Ask AI' : 'Send'}
        </button>
      </form>

      <button onClick={logout} className="lg-out">
        Logout
      </button>
    </div>
  );
} 
 

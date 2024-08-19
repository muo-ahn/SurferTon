// src/App.jsx

import React, { useState } from 'react';
import Match from './Match';
import Chat from './Chat';
import './App.css'

function App() {
  const [userId, setUserId] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [selectedMatchUser, setSelectedMatchUser] = useState(null);

  const handleUserIdChange = (e) => {
    setUserId(e.target.value);
  };

  const handleUserIdSubmit = (e) => {
    e.preventDefault();
    if (userId) {
      setIsSubmitted(true);
      setSelectedMatchUser(null); // Reset selected match when user ID changes
    }
  };

  const generateChatId = (userId1, userId2) => {
    // Ensure the chat_id is always in the format 'chat-X-Y'
    const [X, Y] = [userId1, userId2].sort((a, b) => a - b);
    return `chat-${X}-${Y}`;
  };

  const handleMatchSelection = (user) => {
    setSelectedMatchUser(user);
  };

  return (
    <div className="app-container">
      {!isSubmitted ? (
        <form onSubmit={handleUserIdSubmit}>
          <label htmlFor="user-id-input">Enter User ID: </label>
          <input
            id="user-id-input"
            type="number"
            value={userId}
            onChange={handleUserIdChange}
            placeholder="Enter your user ID"
          />
          <button type="submit">Submit</button>
        </form>
      ) : (
        <>
          {!selectedMatchUser && (
            <Match userId={parseInt(userId)} setSelectedUser={handleMatchSelection} />
          )}
          {selectedMatchUser && (
            <div>
              <h3>Selected User: {selectedMatchUser.name}</h3>
              <Chat
                chatId={generateChatId(parseInt(userId), selectedMatchUser.user_id)}
                userId={parseInt(userId)}
              />
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;

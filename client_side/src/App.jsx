import React from 'react';
import Chat from './Chat';

function App() {
  const chatId = "chat-session-123"; // Example chat ID
  const userId = Math.floor(Math.random() * 4) + 1;

  return (
    <div>
      <Chat chatId={chatId} userId={userId} />
    </div>
  );
}

export default App;

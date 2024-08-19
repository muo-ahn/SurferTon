import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';

function Chat({ chatId, userId }) {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const ws = useRef(null);

  useEffect(() => {
    // Ensure userId is treated as an integer in the WebSocket URL
    ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${chatId}/${parseInt(userId, 10)}`);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [chatId, userId]);

  const sendMessage = () => {
    if (ws.current && message) {
      ws.current.send(message);
      setMessage('');
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      bgcolor="#f0f0f0"
      padding="20px"
    >
      <Paper elevation={3} sx={{ padding: '20px', maxWidth: '600px', width: '100%' }}>
        <Typography variant="h4" gutterBottom>
          1:1 Chat Room
        </Typography>
        <List sx={{ maxHeight: '300px', overflowY: 'auto', marginBottom: '20px' }}>
          {messages.map((msg, index) => (
            <ListItem key={index} divider>
              <ListItemText primary={msg} />
            </ListItem>
          ))}
        </List>
        <TextField
          fullWidth
          label="Type a message"
          variant="outlined"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              sendMessage();
              e.preventDefault();
            }
          }}
          sx={{ marginBottom: '10px' }}
        />
        <Button variant="contained" color="primary" onClick={sendMessage} fullWidth>
          Send
        </Button>
      </Paper>
    </Box>
  );
}

export default Chat;

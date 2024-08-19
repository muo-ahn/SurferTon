import React, { useState, useEffect, useRef } from "react";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardHeader,
  MDBCardBody,
  MDBBtn,
  MDBCardFooter,
  MDBInputGroup,
} from "mdb-react-ui-kit";

function Chat({ chatId, userId }) {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${chatId}/${userId}`);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      const newMessage = event.data;
      setMessages((prevMessages) => [...prevMessages, newMessage]);
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

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const sendMessage = () => {
    if (ws.current && message) {
      ws.current.send(message);
      setMessage('');  // Clear the message input after sending
    }
  };

  return (
    <MDBContainer fluid className="py-5" style={{ backgroundColor: "#eee" }}>
      <MDBRow className="d-flex justify-content-center">
        <MDBCol md="8" lg="6" xl="4">
          <MDBCard>
            <MDBCardHeader
              className="d-flex justify-content-between align-items-center p-3"
              style={{ borderTop: "4px solid #ffa900" }}
            >
              <h5 className="mb-0">Chat messages</h5>
            </MDBCardHeader>

            <div style={{ position: "relative", height: "400px", overflowY: "auto" }}>
              <MDBCardBody>
                {messages.map((msg, index) => {
                  const isUserMessage = msg.startsWith(`User ${userId}`);
                  const messageParts = msg.split(":");
                  const messageSender = messageParts[0] || "Unknown";
                  const messageContent = messageParts[1] ? messageParts[1].trim() : "";
                  const messageTime = new Date().toLocaleTimeString();

                  return (
                    <div key={index} className={`d-flex ${isUserMessage ? 'justify-content-end' : 'justify-content-start'} mb-4`}>
                      <div>
                        <div
                          className={`p-3 ${isUserMessage ? 'text-white bg-primary' : 'text-dark bg-light'} rounded-3`}
                          style={{
                            maxWidth: "300px",
                            borderRadius: "15px",
                            backgroundColor: isUserMessage ? "#007bff" : "#f1f0f0",
                            color: isUserMessage ? "white" : "black",
                          }}
                        >
                          <p className="mb-0">{messageContent}</p>
                        </div>
                        <p className={`small text-muted mt-2 ${isUserMessage ? 'text-right' : ''}`}>{messageTime}</p>
                      </div>
                    </div>
                  );
                })}
                <div ref={messagesEndRef} />
              </MDBCardBody>
            </div>

            <MDBCardFooter className="text-muted d-flex justify-content-start align-items-center p-3">
              <MDBInputGroup className="mb-0">
                <input
                  className="form-control"
                  placeholder="Type message"
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage();
                    }
                  }}
                />
                <MDBBtn color="primary" style={{ paddingTop: ".55rem" }} onClick={sendMessage}>
                  Send
                </MDBBtn>
              </MDBInputGroup>
            </MDBCardFooter>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
}

export default Chat;

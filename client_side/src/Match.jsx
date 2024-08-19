import React, { useState, useEffect } from 'react';

function Match({ userId, setSelectedUser }) {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const response = await fetch(`http://localhost:8000/match/${userId}`);
        if (!response.ok) {
          // Handle HTTP errors
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json(); // Try parsing the response as JSON
        setMatches(data);
      } catch (err) {
        console.error('Failed to fetch matches:', err);
        setError('Failed to load matches. Please check the console for more details.');
      } finally {
        setLoading(false);
      }
    };
  
    fetchMatches();
  }, [userId]);

  if (loading) return <div>Loading matches...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="match-list">
      <h2>Your Matches</h2>
      <ul>
        {matches.map((match, index) => (
          <li key={index}>
            <button onClick={() => setSelectedUser(match.user)}>
              {match.user.name} (Score: {match.score})
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Match;

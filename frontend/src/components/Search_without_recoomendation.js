import React, { useState } from 'react';
import axios from 'axios';

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/search?q=${query}`);
      setResults(res.data);
    } catch (err) {
      console.error("Search error:", err);
      alert("Search failed. Check backend.");
    }
  };

  return (
    <div>
      <h2>🔍 Search Documents</h2>
      <input
        type="text"
        placeholder="Enter keyword or tag"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      <ul>
        {results.map((doc, index) => (
          <li key={index} style={{ marginBottom: '20px' }}>
            <strong>{doc.filename}</strong><br />
            <a href={doc.s3_url} target="_blank" rel="noopener noreferrer">Download</a><br />
            Tags: {doc.tags.join(", ")}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Search;

import React, { useState } from 'react';
import axios from 'axios';

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [relatedDocs, setRelatedDocs] = useState({});

  const handleSearch = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/search?q=${query}`);
      setResults(res.data);
    } catch (err) {
      console.error("Search error:", err);
      alert("Search failed. Check if the backend is running.");
    }
  };

  const handleShowRelated = async (docId) => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/recommend/${docId}`);
      setRelatedDocs((prev) => ({ ...prev, [docId]: res.data }));
    } catch (err) {
      console.error("Recommendation error:", err);
      alert("Could not fetch related documents.");
    }
  };

  const handleDownload = async (filename) => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/download?filename=${encodeURIComponent(filename)}`);
      if (res.data.url) {
        window.open(res.data.url, '_blank');
      } else {
        alert("Download link could not be generated.");
      }
    } catch (err) {
      console.error("Download error:", err);
      alert("Failed to download document.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>🔍 Search Documents</h2>
      <input
        type="text"
        placeholder="Enter keyword or tag"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "300px", marginRight: "10px" }}
      />
      <button onClick={handleSearch}>Search</button>

      <ul style={{ marginTop: "30px" }}>
        {results.map((doc, index) => (
          <li key={index} style={{ marginBottom: '20px' }}>
            <strong>{doc.filename}</strong><br />
            <button onClick={() => handleDownload(doc.filename)}>Download</button><br />
            Tags: {doc.tags.join(", ") || "None"}

            <div style={{ marginTop: '10px' }}>
              <button onClick={() => handleShowRelated(doc._id)}>Show Related</button>
            </div>

            {relatedDocs[doc._id] && relatedDocs[doc._id].length > 0 && (
              <div style={{ marginTop: '10px', paddingLeft: '20px' }}>
                <h4>Related Documents:</h4>
                <ul>
                  {relatedDocs[doc._id].map((relatedDoc, idx) => (
                    <li key={idx}>
                      <strong>{relatedDoc.filename}</strong><br />
                      <button onClick={() => handleDownload(relatedDoc.filename)}>Download</button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Search;


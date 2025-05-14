import React, { useState } from 'react';
import axios from 'axios';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [tags, setTags] = useState('');
  const [uploadStatus, setUploadStatus] = useState('');

  const handleUpload = async () => {
    if (!file || !tags) {
      alert("Please select a file and enter tags.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // Split tags into list
    tags.split(",").forEach(tag => {
      formData.append("tags", tag.trim());
    });

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData);
      setUploadStatus(`✅ File uploaded! URL: ${res.data.url}`);
    } catch (error) {
      console.error("❌ Upload failed:", error);
      setUploadStatus("❌ Upload failed. Please check the backend.");
    }
  };

  return (
    <div style={{ marginBottom: "40px" }}>
      <h2>📤 Upload Document</h2>
      <div>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      </div>
      <div>
        <input
          type="text"
          placeholder="Enter tags (comma separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
        />
      </div>
      <button onClick={handleUpload} style={{ marginTop: "10px" }}>
        Upload
      </button>

      {uploadStatus && (
        <div style={{ marginTop: "15px", color: "green" }}>
          {uploadStatus}
        </div>
      )}
    </div>
  );
};

export default Upload;

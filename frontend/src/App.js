import React from 'react';
import Upload from './components/Upload';
import Search from './components/Search';

function App() {
  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>📄 Smart Document Manager</h1>

      {/* Upload component */}
      <Upload />

      <hr />

      {/* Search + Recommendations */}
      <Search />
    </div>
  );
}

export default App;

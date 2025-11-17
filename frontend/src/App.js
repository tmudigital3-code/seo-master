import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import KeywordUpload from './pages/KeywordUpload';
import KeywordAnalysis from './pages/KeywordAnalysis';
import CompetitorAnalysis from './pages/CompetitorAnalysis';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<KeywordUpload />} />
          <Route path="/analysis" element={<KeywordAnalysis />} />
          <Route path="/competitors" element={<CompetitorAnalysis />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
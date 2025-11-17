import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Plot from 'react-plotly.js';

const Dashboard = () => {
  const [keywords, setKeywords] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from backend API
    const fetchData = async () => {
      try {
        const keywordsResponse = await axios.get('/api/keywords');
        const rankingsResponse = await axios.get('/api/rankings');
        
        setKeywords(keywordsResponse.data);
        setRankings(rankingsResponse.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Prepare data for charts
  const prepareRankingData = () => {
    // Group rankings by platform
    const platformData = {};
    
    rankings.forEach(ranking => {
      if (!platformData[ranking.platform]) {
        platformData[ranking.platform] = [];
      }
      platformData[ranking.platform].push({
        keyword: ranking.keyword_id,
        position: ranking.position,
        visibility: ranking.visibility_score
      });
    });
    
    return platformData;
  };

  if (loading) {
    return <div className="p-6">Loading dashboard data...</div>;
  }

  const rankingData = prepareRankingData();

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">SEO Keyword Tracking Dashboard</h1>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">Total Keywords</h3>
          <p className="text-3xl font-bold text-blue-600">{keywords.length}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">Avg. Position</h3>
          <p className="text-3xl font-bold text-green-600">
            {rankings.length > 0 
              ? (rankings.reduce((sum, r) => sum + (r.position || 0), 0) / rankings.length).toFixed(1)
              : 'N/A'}
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">Visibility Score</h3>
          <p className="text-3xl font-bold text-purple-600">
            {rankings.length > 0 
              ? (rankings.reduce((sum, r) => sum + (r.visibility_score || 0), 0) / rankings.length).toFixed(1)
              : 'N/A'}%
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">Top Platform</h3>
          <p className="text-3xl font-bold text-orange-600">Google</p>
        </div>
      </div>
      
      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Ranking Comparison Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Ranking Comparison</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={Object.keys(rankingData).map(platform => ({
                name: platform,
                avgPosition: rankingData[platform].reduce((sum, r) => sum + (r.position || 0), 0) / rankingData[platform].length
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="avgPosition" fill="#8884d8" name="Average Position" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Visibility Score Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Visibility Score by Platform</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={Object.keys(rankingData).map(platform => ({
                name: platform,
                avgVisibility: rankingData[platform].reduce((sum, r) => sum + (r.visibility || 0), 0) / rankingData[platform].length
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="avgVisibility" stroke="#82ca9d" name="Avg Visibility (%)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      {/* Keyword Table */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Keyword Performance</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Keyword</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Difficulty</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Google Pos</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Visibility</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {keywords.map((keyword) => (
                <tr key={keyword.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{keyword.keyword}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{keyword.volume || 'N/A'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{keyword.difficulty || 'N/A'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {rankings.filter(r => r.keyword_id === keyword.id && r.platform === 'google')[0]?.position || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {rankings.filter(r => r.keyword_id === keyword.id && r.platform === 'google')[0]?.visibility_score?.toFixed(1) || 'N/A'}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button className="text-blue-600 hover:text-blue-900">Analyze</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
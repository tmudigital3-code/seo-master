import React, { useState } from 'react';
import axios from 'axios';

const KeywordUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file to upload');
      return;
    }

    setUploading(true);
    setUploadResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // In a real application, you would send this to your backend API
      // const response = await axios.post('/api/upload-keywords', formData, {
      //   headers: {
      //     'Content-Type': 'multipart/form-data'
      //   }
      // });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setUploadResult({
        success: true,
        message: `Successfully uploaded ${file.name}. Processing started for 25 keywords.`,
        keywordCount: 25
      });
    } catch (error) {
      setUploadResult({
        success: false,
        message: 'Upload failed. Please try again.'
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Upload Keywords</h1>
      
      <div className="bg-white p-6 rounded-lg shadow max-w-2xl">
        <h2 className="text-xl font-bold mb-4">Upload CSV File</h2>
        
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select CSV file with keywords
          </label>
          
          <div className="flex items-center">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
          </div>
          
          {file && (
            <p className="mt-2 text-sm text-gray-500">
              Selected file: {file.name} ({(file.size / 1024).toFixed(2)} KB)
            </p>
          )}
        </div>
        
        <div className="mb-6">
          <h3 className="text-lg font-medium mb-2">Required CSV Format</h3>
          <div className="bg-gray-50 p-4 rounded-md">
            <pre className="text-sm text-gray-600">
{`Keyword,Target URL,Search Country,Volume,Difficulty,CPC,Intent
best seo tools,https://example.com/seo-tools,us,1000,65,5.2,commercial
keyword research tips,https://example.com/keywords,uk,800,45,3.1,informational
...`}
            </pre>
          </div>
        </div>
        
        <button
          onClick={handleUpload}
          disabled={uploading || !file}
          className={`px-6 py-3 rounded-md text-white font-medium ${
            uploading || !file
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {uploading ? 'Uploading...' : 'Upload Keywords'}
        </button>
        
        {uploadResult && (
          <div className={`mt-6 p-4 rounded-md ${uploadResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
            <p className="font-medium">{uploadResult.message}</p>
            {uploadResult.keywordCount && (
              <p className="mt-2">Keywords will be processed in the background. Check the dashboard for updates.</p>
            )}
          </div>
        )}
      </div>
      
      <div className="mt-8 bg-white p-6 rounded-lg shadow max-w-2xl">
        <h2 className="text-xl font-bold mb-4">Manual Entry</h2>
        <p className="text-gray-600 mb-4">Enter keywords manually if you prefer not to upload a CSV file.</p>
        
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Keyword</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Enter keyword"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Target URL</label>
              <input
                type="url"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="https://example.com/page"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Search Country</label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md">
                <option value="us">United States</option>
                <option value="uk">United Kingdom</option>
                <option value="ca">Canada</option>
                <option value="au">Australia</option>
                <option value="de">Germany</option>
              </select>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Volume</label>
              <input
                type="number"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="1000"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Difficulty (0-100)</label>
              <input
                type="number"
                min="0"
                max="100"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="50"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">CPC ($)</label>
              <input
                type="number"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="2.50"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Search Intent</label>
            <select className="w-full px-3 py-2 border border-gray-300 rounded-md">
              <option value="">Select intent</option>
              <option value="informational">Informational</option>
              <option value="commercial">Commercial</option>
              <option value="transactional">Transactional</option>
              <option value="navigational">Navigational</option>
            </select>
          </div>
          
          <button
            type="button"
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Add Keyword
          </button>
        </form>
      </div>
    </div>
  );
};

export default KeywordUpload;
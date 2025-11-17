import React, { useState } from 'react';

const Settings = () => {
  const [settings, setSettings] = useState({
    scrapeFrequency: 'daily',
    emailNotifications: true,
    slackNotifications: false,
    whatsappNotifications: false,
    alertThreshold: 5,
    countryCode: 'us',
    apiKey: '',
    serpApiKey: '',
    openaiApiKey: '',
    geminiApiKey: ''
  });

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSave = () => {
    // In a real application, you would save these settings to your backend
    console.log('Saving settings:', settings);
    alert('Settings saved successfully!');
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Settings</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* General Settings */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">General Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Scraping Frequency
              </label>
              <select
                name="scrapeFrequency"
                value={settings.scrapeFrequency}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="hourly">Hourly</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Default Country Code
              </label>
              <select
                name="countryCode"
                value={settings.countryCode}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="us">United States</option>
                <option value="uk">United Kingdom</option>
                <option value="ca">Canada</option>
                <option value="au">Australia</option>
                <option value="de">Germany</option>
                <option value="fr">France</option>
                <option value="jp">Japan</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Alert Position Drop Threshold
              </label>
              <div className="flex items-center">
                <input
                  type="number"
                  name="alertThreshold"
                  value={settings.alertThreshold}
                  onChange={handleInputChange}
                  min="1"
                  max="50"
                  className="w-20 px-3 py-2 border border-gray-300 rounded-md"
                />
                <span className="ml-2 text-gray-600">positions</span>
              </div>
              <p className="mt-1 text-sm text-gray-500">
                Get alerted when a keyword drops by this many positions
              </p>
            </div>
          </div>
        </div>
        
        {/* Notification Settings */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Notifications</h2>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                name="emailNotifications"
                checked={settings.emailNotifications}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 rounded"
              />
              <label className="ml-2 block text-sm text-gray-700">
                Email Notifications
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                type="checkbox"
                name="slackNotifications"
                checked={settings.slackNotifications}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 rounded"
              />
              <label className="ml-2 block text-sm text-gray-700">
                Slack Notifications
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                type="checkbox"
                name="whatsappNotifications"
                checked={settings.whatsappNotifications}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 rounded"
              />
              <label className="ml-2 block text-sm text-gray-700">
                WhatsApp Notifications
              </label>
            </div>
            
            <div className="pt-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Notification Email
              </label>
              <input
                type="email"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="your@email.com"
              />
              <p className="mt-1 text-sm text-gray-500">
                Email address for notifications
              </p>
            </div>
          </div>
        </div>
        
        {/* API Keys */}
        <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">API Keys</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                SERP API Key
              </label>
              <input
                type="password"
                name="serpApiKey"
                value={settings.serpApiKey}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Enter your SERP API key"
              />
              <p className="mt-1 text-sm text-gray-500">
                For Google, Bing, and other search engine rankings
              </p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                OpenAI API Key
              </label>
              <input
                type="password"
                name="openaiApiKey"
                value={settings.openaiApiKey}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Enter your OpenAI API key"
              />
              <p className="mt-1 text-sm text-gray-500">
                For content generation and analysis
              </p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Gemini API Key
              </label>
              <input
                type="password"
                name="geminiApiKey"
                value={settings.geminiApiKey}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Enter your Gemini API key"
              />
              <p className="mt-1 text-sm text-gray-500">
                For competitor content analysis
              </p>
            </div>
          </div>
          
          <div className="mt-6">
            <button
              onClick={handleSave}
              className="px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700"
            >
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
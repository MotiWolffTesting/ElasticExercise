import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import ResultsViewer from './components/ResultsViewer';
import ProcessingStatus from './components/ProcessingStatus';
import { fetchProcessingStatus, fetchAntisemiticWithWeapons, fetchMultipleWeapons } from './services/api';

function App() {
  const [status, setStatus] = useState(null);
  const [antisemiticResults, setAntisemiticResults] = useState([]);
  const [multipleWeaponsResults, setMultipleWeaponsResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const statusData = await fetchProcessingStatus();
      setStatus(statusData);
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProcessData = async () => {
    try {
      setLoading(true);
      // This would trigger the processing endpoint
      // For now, we'll just reload the status
      await loadInitialData();
    } catch (error) {
      console.error('Error processing data:', error);
    }
  };

  const loadAntisemiticResults = async () => {
    try {
      setLoading(true);
      const results = await fetchAntisemiticWithWeapons();
      setAntisemiticResults(results.documents || []);
    } catch (error) {
      console.error('Error loading antisemitic results:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMultipleWeaponsResults = async () => {
    try {
      setLoading(true);
      const results = await fetchMultipleWeapons();
      setMultipleWeaponsResults(results.documents || []);
    } catch (error) {
      console.error('Error loading multiple weapons results:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <nav className="flex space-x-8 mb-8">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-3 py-2 rounded-md text-sm font-medium ${
              activeTab === 'dashboard'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setActiveTab('antisemitic')}
            className={`px-3 py-2 rounded-md text-sm font-medium ${
              activeTab === 'antisemitic'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Antisemitic with Weapons
          </button>
          <button
            onClick={() => setActiveTab('multiple-weapons')}
            className={`px-3 py-2 rounded-md text-sm font-medium ${
              activeTab === 'multiple-weapons'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Multiple Weapons
          </button>
        </nav>

        {activeTab === 'dashboard' && (
          <Dashboard 
            status={status} 
            onProcessData={handleProcessData}
            loading={loading}
          />
        )}
        
        {activeTab === 'antisemitic' && (
          <ResultsViewer
            title="Antisemitic Documents with Weapons"
            results={antisemiticResults}
            onLoadData={loadAntisemiticResults}
            loading={loading}
          />
        )}
        
        {activeTab === 'multiple-weapons' && (
          <ResultsViewer
            title="Documents with Multiple Weapons"
            results={multipleWeaponsResults}
            onLoadData={loadMultipleWeaponsResults}
            loading={loading}
          />
        )}
      </div>
    </div>
  );
}

export default App;
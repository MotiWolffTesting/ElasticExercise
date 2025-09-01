import React, { useState, useEffect } from 'react';

function ResultsViewer({ title, results, onLoadData, loading }) {
  const [expandedItems, setExpandedItems] = useState(new Set());

  useEffect(() => {
    if (results.length === 0) {
      onLoadData();
    }
  }, [results, onLoadData]);

  const toggleExpanded = (index) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedItems(newExpanded);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString();
    } catch {
      return dateString;
    }
  };

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            {title}
          </h3>
          <button
            onClick={onLoadData}
            disabled={loading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Refresh Data'}
          </button>
        </div>

        {loading && (
          <div className="text-center py-8">
            <div className="inline-flex items-center px-4 py-2 text-sm text-gray-500">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading results...
            </div>
          </div>
        )}

        {!loading && results.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500">No results found. Click "Refresh Data" to load results.</p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <div className="space-y-4">
            <div className="text-sm text-gray-500">
              Found {results.length} documents
            </div>
            
            <div className="space-y-3">
              {results.slice(0, 50).map((result, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          result.is_antisemitic ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                        }`}>
                          {result.is_antisemitic ? 'Antisemitic' : 'Not Antisemitic'}
                        </span>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          result.sentiment === 'negative' ? 'bg-red-100 text-red-800' :
                          result.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {result.sentiment}
                        </span>
                        {result.weapon_count > 0 && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                            {result.weapon_count} weapon(s)
                          </span>
                        )}
                      </div>
                      
                      <p className="text-sm text-gray-900 mb-2">
                        {expandedItems.has(index) ? result.text : `${result.text.substring(0, 200)}...`}
                      </p>
                      
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>Date: {formatDate(result.created_at)}</span>
                        {result.detected_weapons && result.detected_weapons.length > 0 && (
                          <span>Weapons: {result.detected_weapons.join(', ')}</span>
                        )}
                      </div>
                    </div>
                    
                    <button
                      onClick={() => toggleExpanded(index)}
                      className="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-600"
                    >
                      {expandedItems.has(index) ? 'Show Less' : 'Show More'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
            
            {results.length > 50 && (
              <div className="text-center py-4 text-sm text-gray-500">
                Showing first 50 results of {results.length} total documents
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsViewer;
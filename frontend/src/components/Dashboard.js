import React from 'react';
import ProcessingStatus from './ProcessingStatus';
import StatisticsCard from './StatisticsCard';
import DataChart from './DataChart';

function Dashboard({ status, onProcessData, loading }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            System Overview
          </h3>
          
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-6">
            <StatisticsCard
              title="Processing Status"
              value={status?.status || 'Unknown'}
              color={getStatusColor(status?.status)}
            />
            <StatisticsCard
              title="Total Documents"
              value={status?.total_count || 0}
              color="bg-blue-100 text-blue-800"
            />
            <StatisticsCard
              title="Processed Documents"
              value={status?.processed_count || 0}
              color="bg-green-100 text-green-800"
            />
          </div>

          <div className="flex space-x-4">
            <button
              onClick={onProcessData}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Process Data'}
            </button>
            
            <button
              onClick={() => window.location.reload()}
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Refresh Status
            </button>
          </div>
        </div>
      </div>

      {status && (
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Processing Details
            </h3>
            <ProcessingStatus status={status} />
          </div>
        </div>
      )}

      {status?.status === 'completed' && (
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Data Visualization
            </h3>
            <DataChart status={status} />
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
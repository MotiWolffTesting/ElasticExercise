import React from 'react';

function ProcessingStatus({ status }) {
  if (!status) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-500">Status:</span>
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          status.status === 'completed' ? 'bg-green-100 text-green-800' :
          status.status === 'processing' ? 'bg-yellow-100 text-yellow-800' :
          status.status === 'error' ? 'bg-red-100 text-red-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {status.status}
        </span>
      </div>
      
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-500">Message:</span>
        <span className="text-sm text-gray-900">{status.message}</span>
      </div>
      
      {status.processed_count !== undefined && (
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-500">Processed:</span>
          <span className="text-sm text-gray-900">{status.processed_count}</span>
        </div>
      )}
      
      {status.total_count !== undefined && (
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-500">Total:</span>
          <span className="text-sm text-gray-900">{status.total_count}</span>
        </div>
      )}
    </div>
  );
}

export default ProcessingStatus;
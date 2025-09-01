import React from 'react';

function Header() {
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center">
            <h1 className="text-3xl font-bold text-gray-900">
              Malicious Text Analysis
            </h1>
          </div>
          <div className="text-sm text-gray-500">
            ElasticSearch + React Dashboard
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
import React, { useState } from 'react';
import IngestForm from './components/IngestForm';
import ChatInterface from './components/ChatInterface';

function App() {
  const [hasIngested, setHasIngested] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-900">
      {!hasIngested ? (
        <div className="pt-20">
          <IngestForm onIngestSuccess={() => setHasIngested(true)} />
        </div>
      ) : (
        <ChatInterface />
      )}
    </div>
  );
}

export default App;

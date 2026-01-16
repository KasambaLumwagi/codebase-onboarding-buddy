import React, { useState } from 'react';
import IngestForm from './components/IngestForm';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
import ErrorBoundary from './components/ErrorBoundary';

function App() {
  const [sessionId, setSessionId] = useState(null);

  return (
    <ErrorBoundary>
      <div className="dark">
        <div className="flex min-h-screen bg-gray-100 dark:bg-gray-900 font-sans text-gray-900 dark:text-gray-100">
          <Sidebar onSelectSession={setSessionId} currentSessionId={sessionId} />

          <div className="flex-1 flex flex-col">
            {!sessionId ? (
              <div className="flex-1 pt-20">
                <IngestForm onIngestSuccess={(id) => setSessionId(id)} />
              </div>
            ) : (
              <ChatInterface sessionId={sessionId} />
            )}
          </div>
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;

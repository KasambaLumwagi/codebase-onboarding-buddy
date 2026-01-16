import React, { useEffect, useState } from 'react';
import { getSessions, deleteSession } from '../api';

export default function Sidebar({ onSelectSession, currentSessionId }) {
    const [sessions, setSessions] = useState([]);

    useEffect(() => {
        loadSessions();
    }, []);

    const loadSessions = async () => {
        try {
            const data = await getSessions();
            setSessions(data);
        } catch (e) {
            console.error(e);
        }
    };

    const handleDelete = async (e, sessionId) => {
        e.stopPropagation(); // Prevent selecting the session
        if (!window.confirm("Delete this chat history?")) return;
        try {
            await deleteSession(sessionId);
            loadSessions(); // Reload list
            if (currentSessionId === sessionId) {
                window.location.reload(); // Simple way to clear current state if deleted
            }
        } catch (err) {
            alert("Failed to delete: " + err.message);
        }
    };

    return (
        <div className="w-64 bg-gray-900 text-white h-screen flex flex-col border-r border-gray-800">
            <div className="p-4 border-b border-gray-800 font-bold flex justify-between items-center bg-gray-900">
                <span>History</span>
                <button
                    onClick={() => onSelectSession(null)}
                    className="text-xs bg-indigo-600 hover:bg-indigo-700 text-white px-2 py-1 rounded"
                    title="New Chat"
                >
                    + New
                </button>
            </div>
            <div className="flex-1 overflow-y-auto p-2 space-y-2 bg-gray-900">
                {sessions.map(s => (
                    <div
                        key={s.id}
                        onClick={() => onSelectSession(s.id)}
                        className={`group p-2 rounded cursor-pointer text-sm truncate flex justify-between items-center transition-colors ${currentSessionId === s.id ? 'bg-indigo-700' : 'hover:bg-gray-800'}`}
                    >
                        <div className="truncate">
                            {s.repo.split('/').pop()}
                            <div className="text-xs text-gray-500">
                                {new Date(s.date).toLocaleDateString()} • {s.message_count} msgs
                            </div>
                        </div>
                        <button
                            onClick={(e) => handleDelete(e, s.id)}
                            className="text-gray-400 hover:text-red-400 opacity-0 group-hover:opacity-100 px-2"
                            title="Delete"
                        >
                            ✕
                        </button>
                    </div>
                ))}
                {sessions.length === 0 && <div className="text-gray-500 text-xs p-2">No history yet.</div>}
            </div>
        </div>
    );
}

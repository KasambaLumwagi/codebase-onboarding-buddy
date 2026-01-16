import React, { useState } from 'react';
import { sendMessage } from '../api';

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'model', text: 'I have analyzed the codebase. You can now ask me questions about "Where is the auth logic?" or "How do I add a new API route?".' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = input;
        setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
        setInput('');
        setLoading(true);

        try {
            const data = await sendMessage(userMsg);
            setMessages(prev => [...prev, { role: 'model', text: data.response }]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'model', text: `Error: ${err.message}` }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto bg-gray-50 shadow-xl">
            <div className="p-4 bg-indigo-700 text-white shadow-md">
                <h1 className="text-xl font-bold">Codebase Onboarding Buddy</h1>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-2xl p-3 rounded-lg ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white text-gray-800 shadow border'}`}>
                            <pre className="whitespace-pre-wrap font-sans text-sm">{msg.text}</pre>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white p-3 rounded-lg shadow border text-gray-500 text-sm">
                            Thinking...
                        </div>
                    </div>
                )}
            </div>

            <div className="p-4 bg-white border-t">
                <form onSubmit={handleSend} className="flex gap-2">
                    <input
                        type="text"
                        className="flex-1 p-2 border rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        placeholder="Ask a question about the code..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}

// pages/index.js
'use client';
import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Home() {
  const [repoUrl, setRepoUrl] = useState('');
  const [prompt, setPrompt] = useState('');
  const [logs, setLogs] = useState([]);
  const [fixes, setFixes] = useState([]);

  useEffect(() => {
    const savedFixes = localStorage.getItem('backspace_fixes');
    if (savedFixes) setFixes(JSON.parse(savedFixes));
  }, []);

  const addFix = (fix) => {
    const updated = [...fixes, fix];
    setFixes(updated);
    localStorage.setItem('backspace_fixes', JSON.stringify(updated));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLogs([]);
    const eventSource = new EventSource('/api/code-stream?repoUrl=' + encodeURIComponent(repoUrl) + '&prompt=' + encodeURIComponent(prompt));

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.message) {
          setLogs((prev) => [...prev, data.message]);
        }
        if (data.pr_url) {
          addFix({ prompt, prUrl: data.pr_url });
          eventSource.close();
        }
      } catch (error) {
        // Handle plain text messages as fallback
        setLogs((prev) => [...prev, event.data]);
      }
    };

    eventSource.onerror = () => {
      setLogs((prev) => [...prev, '❌ Error during execution']);
      eventSource.close();
    };
  };

  return (
    <div className="min-h-screen bg-neutral-50 text-neutral-900 font-sans">
      <Head>
        <title>Backspace Coding Agent</title>
      </Head>
      <main className="flex flex-col items-center justify-center py-20 px-4">
        <h1 className="text-3xl font-semibold mb-6 tracking-tight">Backspace Coding Agent</h1>

        <form onSubmit={handleSubmit} className="w-full max-w-xl text-center space-y-4">
          <input
            type="text"
            placeholder="Enter GitHub Repo URL"
            className="w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring focus:border-black"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            required
          />
          <textarea
            placeholder="Enter your coding prompt..."
            className="w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring focus:border-black"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={3}
            required
          />
          <button
            type="submit"
            className="bg-black text-white px-6 py-2 rounded-xl hover:bg-neutral-800 transition"
          >
            Run Agent
          </button>
        </form>

        <div className="w-full max-w-xl mt-8 text-sm bg-white border rounded-xl p-4 shadow-sm">
          <h2 className="text-md font-medium mb-2">⏱️ Live Agent Stream</h2>
          <div className="space-y-1 max-h-64 overflow-y-auto">
            {logs.map((log, idx) => (
              <div key={idx} className="font-mono text-neutral-700">{log}</div>
            ))}
          </div>
        </div>

        {fixes.length > 0 && (
          <div className="w-full max-w-xl mt-12 text-center">
            <h2 className="text-lg font-semibold mb-2">🔧 Fixes for You</h2>
            <ul className="space-y-2">
              {fixes.map((fix, idx) => (
                <li key={idx} className="flex justify-between items-center px-4 py-2 border rounded-xl bg-white shadow-sm">
                  <span className="text-left">🧩 {fix.prompt}</span>
                  <a href={fix.prUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                    View PR
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}

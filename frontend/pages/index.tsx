import { useState } from 'react';
import Head from 'next/head';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useRagStore } from '../state/store';

const queryClient = new QueryClient();

export default function Home() {
  const [question, setQuestion] = useState('');
  const { ask, messages } = useRagStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await ask(question);
    setQuestion('');
  };

  return (
    <QueryClientProvider client={queryClient}>
      <Head>
        <title>Volvo RAG Demo</title>
      </Head>
      <header className="p-4 flex items-center space-x-4 shadow">
        <img src="/volvo-logo.svg" alt="Volvo" className="h-8" />
        <h1 className="text-xl font-bold">Volvo RAG</h1>
      </header>
      <main className="p-4">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            className="border rounded flex-1 p-2"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question"
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded" type="submit">
            Ask
          </button>
        </form>
        <div className="mt-4 space-y-2">
          {messages.map((msg, idx) => (
            <div key={idx} className="p-2 bg-gray-100 rounded">
              {msg}
            </div>
          ))}
        </div>
      </main>
    </QueryClientProvider>
  );
}

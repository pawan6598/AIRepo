import create from 'zustand';

interface RagState {
  messages: string[];
  ask: (question: string) => Promise<void>;
}

export const useRagStore = create<RagState>((set) => ({
  messages: [],
  ask: async (question: string) => {
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      set((state) => ({ messages: [...state.messages, `Q: ${question}`, `A: ${data.answer}`] }));
    } catch (err) {
      set((state) => ({ messages: [...state.messages, 'Error fetching answer'] }));
    }
  },
}));

import React, { useEffect, useState } from 'react';
import { api } from '../../lib/api';

type Habit = { id: string; title: string; frequency: string; target: number };

export default function HabitCard() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHabits = async () => {
      const res = await api('/habits')
      setHabits(res.data)
    }
    fetchHabits()
  }, []);

  if (error) return <div className="p-4 border rounded">{error}</div>;
  return (
    <>
      {habits.map((h) => (
        <a key={h.id} href={`/habit/${h.id}`} className="p-4 border rounded flex flex-col gap-2 bg-white dark:bg-neutral-900">
          <div className="font-medium">{h.title}</div>
          <div className="text-sm opacity-70">{h.frequency} • target {h.target}</div>
          <button onClick={async (e) => { 
            e.preventDefault(); 
            await api.post(`/habits/${h.id}/log`, {}); 
          }} 
          className="mt-2 inline-flex items-center justify-center bg-green-600 text-white rounded px-3 py-1 text-sm"
          >
            Quick Log
          </button>
        </a>
      ))}
    </>
  );
}



import React, { useEffect, useState } from 'react';
import { api } from '../../lib/api';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

type Data = { labels: string[]; datasets: { label: string; data: number[] }[] };

export default function ProgressChart() {
  const [data, setData] = useState<Data | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      const res = await api('/stats/overview')
      setData(res.data)
    }
    fetchStats()
  }, []);

  if (error) return <div className="p-4 border rounded">{error}</div>;
  if (!data) return <div className="p-4 border rounded bg-white dark:bg-neutral-900" suppressHydrationWarning>Loading chart...</div>;
  const points = data.labels.map((l, i) => ({ name: l, value: data.datasets[0]?.data[i] ?? 0 }));
  
  return (
    <div className="p-4 border rounded bg-white dark:bg-neutral-900">
      <div className="mb-2 font-medium">Last 7 days</div>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={points}>
          <XAxis dataKey="name" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}



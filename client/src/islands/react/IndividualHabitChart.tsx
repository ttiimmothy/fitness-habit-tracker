import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useHabitStore } from '../../store/habitStore';
import { useHabitDailyProgress, HabitDailyProgress } from '../../hooks/useHabits';

// Chart data type for recharts
type ChartDataPoint = {
  date: string;
  progress: number;
};

// Custom Tooltip component for better dark mode styling
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const isCompleted = payload[0].value > 0;
    return (
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg p-3">
        <p className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-1">
          {new Date(label).toLocaleDateString('en-US', { 
            weekday: 'long', 
            month: 'short', 
            day: 'numeric' 
          })}
        </p>
        <p className={`text-sm font-semibold ${isCompleted ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
          {isCompleted ? '✓ Completed' : '✗ Not completed'}
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Progress: {payload[0].value}
        </p>
      </div>
    );
  }
  return null;
};

export default function IndividualHabitChart() {
  const { selectedHabit } = useHabitStore();
  
  // Fetch daily progress data for the selected habit
  const { 
    data: dailyProgress, 
    isLoading, 
    error 
  } = useHabitDailyProgress(selectedHabit?.id || '', 7);

  // Transform API data to chart format
  const chartData: ChartDataPoint[] = dailyProgress?.map((day: HabitDailyProgress) => ({
    date: day.date,
    progress: day.actual
  })) || [];

  if (!selectedHabit) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="text-center py-8">
          <div className="text-gray-500 dark:text-gray-400 mb-2">
            <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-1">No habit selected</h3>
          <p className="text-gray-500 dark:text-gray-400">Select a habit to view its progress</p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900 text-red-600 dark:text-red-400">
        {error?.message || 'Failed to load habit progress'}
      </div>
    );
  }

  return (
    <div className="p-4 border rounded bg-white dark:bg-neutral-900">
      <div className="mb-4">
        <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-1">
          {selectedHabit.title} - Last 7 days
        </h3>
        <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
          <span>Target: {selectedHabit.target}</span>
          <span>•</span>
          <span>Completed: {dailyProgress?.filter(day => day.completed).length || 0}/7 days</span>
          <span>•</span>
          <span>Success Rate: {dailyProgress ? Math.round((dailyProgress.filter(day => day.completed).length / dailyProgress.length) * 100) : 0}%</span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <XAxis 
            dataKey="date" 
            tick={{ fill: 'currentColor', fontSize: 12 }}
            axisLine={{ stroke: 'currentColor' }}
            tickFormatter={(value) => {
              const date = new Date(value);
              return date.toLocaleDateString('en-US', { weekday: 'short' });
            }}
          />
          <YAxis 
            allowDecimals={false} 
            tick={{ fill: 'currentColor', fontSize: 12 }}
            axisLine={{ stroke: 'currentColor' }}
            domain={[0, selectedHabit.target]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line 
            type="monotone" 
            dataKey="progress" 
            stroke={selectedHabit.color || '#3B82F6'} 
            strokeWidth={3}
            dot={{ r: 5, fill: selectedHabit.color || '#3B82F6' }}
            activeDot={{ r: 7, fill: selectedHabit.color || '#3B82F6' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

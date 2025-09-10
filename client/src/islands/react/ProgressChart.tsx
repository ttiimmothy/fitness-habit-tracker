import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useHabits, HabitDailyProgress } from '../../hooks/useHabits';
import {useMultipleHabitsDailyProgress} from "../../hooks/useStats";

// Chart data type for recharts
type ChartDataPoint = {
  date: string;
  [habitTitle: string]: string | number;
};

// Custom Tooltip component for better dark mode styling
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg p-3">
        <p className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
          {new Date(label).toLocaleDateString('en-US', { 
            weekday: 'long', 
            month: 'short', 
            day: 'numeric' 
          })}
        </p>
        {payload.map((entry: any, index: number) => {
          const isCompleted = entry.value > 0;
          return (
            <div key={index} className="flex items-center gap-2 mb-1">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: entry.color }}
              />
              <p className="text-sm" style={{ color: entry.color }}>
                {entry.dataKey}: <span className="font-semibold">
                  {isCompleted ? '✓ Completed' : '✗ Not completed'}
                </span>
              </p>
            </div>
          );
        })}
      </div>
    );
  }
  return null;
};

export default function ProgressChart() {
  const { data: habits, isLoading: habitsLoading, error: habitsError } = useHabits();
  
  // Get habit IDs for fetching daily progress
  const habitIds = habits?.map(habit => habit.id) || [];
  
  // Fetch daily progress for all habits
  const { 
    data: dailyProgressData, 
    isLoading: dailyProgressLoading, 
    error: dailyProgressError 
  } = useMultipleHabitsDailyProgress(habitIds, 7);

  // Transform API data to chart format
  const createChartData = (): ChartDataPoint[] => {
    if (!habits || !dailyProgressData || habits.length === 0) return [];

    // Get all unique dates from the first habit's data (all habits should have same dates)
    const firstHabitId = habits[0]?.id;
    const firstHabitData = dailyProgressData[firstHabitId] || [];
    
    if (firstHabitData.length === 0) return [];

    // Create chart data by combining all habits' daily progress
    const chartData: ChartDataPoint[] = firstHabitData.map((day: HabitDailyProgress) => {
      const dataPoint: ChartDataPoint = { date: day.date };
      
      // Add each habit's progress for this date
      habits.forEach(habit => {
        const habitData = dailyProgressData[habit.id] || [];
        const habitDay = habitData.find((d: HabitDailyProgress) => d.date === day.date);
        dataPoint[habit.title] = habitDay?.actual || 0;
      });
      
      return dataPoint;
    });

    return chartData;
  };

  const chartData = createChartData();

  // Generate colors for habits
  const getHabitColor = (index: number) => {
    const colors = [
      '#3B82F6', // Blue
      '#10B981', // Green
      '#F59E0B', // Yellow
      '#EF4444', // Red
      '#8B5CF6', // Purple
      '#F97316', // Orange
      '#06B6D4', // Cyan
      '#84CC16', // Lime
      '#EC4899', // Pink
      '#6366F1', // Indigo
    ];
    return colors[index % colors.length];
  };

  if (habitsLoading || dailyProgressLoading) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (habitsError || dailyProgressError) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900 text-red-600 dark:text-red-400">
        {habitsError ? 'Failed to load habits.' : 'Failed to load habit progress data.'}
      </div>
    );
  }

  if (!habits || habits.length === 0) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="text-center py-8">
          <div className="text-gray-500 dark:text-gray-400 mb-2">
            <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-1">No habits yet</h3>
          <p className="text-gray-500 dark:text-gray-400">Create your first habit to see progress tracking!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 border rounded bg-white dark:bg-neutral-900">
      <div className="mb-4 font-medium">Habit Progress - Last 7 days</div>
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
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          {habits.map((habit, index) => (
            <Line
              key={habit.id}
              type="monotone"
              dataKey={habit.title}
              stroke={habit.color || getHabitColor(index)}
              strokeWidth={2}
              dot={{ r: 4 }}
              name={habit.title}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}



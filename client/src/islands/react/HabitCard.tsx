import React, { useState } from 'react';
import { useHabits } from '../../hooks/useHabits';
import { useHabitStore } from '../../store/habitStore';
import AddHabitButton from './AddHabitButton';
import {useLogHabit, useTodayHabitLogs} from "../../hooks/useHabitLog";

export default function HabitCard() {
  const { data: habits, isLoading, error } = useHabits();
  const { data: todayLogs, isLoading: todayLogsLoading } = useTodayHabitLogs();
  const logHabitMutation = useLogHabit();
  const [loggingHabits, setLoggingHabits] = useState<Set<string>>(new Set());
  const { setSelectedHabit } = useHabitStore();

  const handleQuickLog = async (e: React.MouseEvent, habitId: string) => {
    e.preventDefault();
    
    // Add habit to logging set
    setLoggingHabits(prev => new Set(prev).add(habitId));
    
    try {
      await logHabitMutation.mutateAsync(habitId);
    } catch (error) {
      console.error('Failed to log habit:', error);
    } finally {
      // Remove habit from logging set
      setLoggingHabits(prev => {
        const newSet = new Set(prev);
        newSet.delete(habitId);
        return newSet;
      });
    }
  };

  const handleHabitClick = (habit: any) => {
    setSelectedHabit(habit);
  };

  // Helper function to check if a habit is already logged today
  const isHabitLoggedToday = (habitId: string) => {
    if (!todayLogs) return false;
    const todayLog = todayLogs.find(log => log.habit_id === habitId);
    return todayLog?.logged_today || false;
  };

  if (isLoading || todayLogsLoading) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900 text-red-600 dark:text-red-400">
        Failed to load habits. Please try again.
      </div>
    );
  }

  return (
    <>
      {/* Add Habit Button */}
      <AddHabitButton />
      
      {/* Existing Habits */}
      {habits?.map((habit) => (
        <a 
          key={habit.id} 
          href={`/habit/${habit.id}`} 
          onClick={() => handleHabitClick(habit)}
          className="p-4 border rounded flex flex-col gap-2 bg-white dark:bg-neutral-900 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <div className="font-medium text-gray-900 dark:text-gray-100">{habit.title}</div>
                {/* {habit.color && (
                  <div 
                    className="w-3 h-3 rounded-full flex-shrink-0"
                    style={{ backgroundColor: habit.color }}
                  />
                )} */}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-2 h-5">
                {habit.description ?? ""}
              </div>
              {/* Category Badge */}
              <div className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                {habit.category}
              </div>
            </div>
          </div>
          
          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
            <span className="capitalize">{habit.frequency}</span>
            {/* <span>•</span> */}
            <span>Target: {habit.target}</span>
          </div>
          
          <button 
            onClick={(e) => handleQuickLog(e, habit.id)}
            disabled={loggingHabits.has(habit.id) || isHabitLoggedToday(habit.id)}
            className={`mt-2 inline-flex items-center justify-center rounded px-3 py-1 text-sm transition-colors ${
              isHabitLoggedToday(habit.id)
                ? 'bg-gray-500 text-white cursor-not-allowed'
                : loggingHabits.has(habit.id)
                ? 'bg-green-400 text-white cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700 text-white'
            }`}
          >
            {isHabitLoggedToday(habit.id) 
              ? '✓ Logged Today' 
              : loggingHabits.has(habit.id) 
              ? 'Logging...' 
              : 'Quick Log'
            }
          </button>
        </a>
      ))}
      
      {/* Empty State */}
      {habits && habits.length === 0 && (
        <div className="p-8 text-center bg-white dark:bg-neutral-900 border rounded">
          <div className="text-gray-500 dark:text-gray-400 mb-2">
            <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-1">No habits yet</h3>
          <p className="text-gray-500 dark:text-gray-400">Create your first habit to get started!</p>
        </div>
      )}
    </>
  );
}



import React from 'react';
import { useHabitStore } from '../../store/habitStore';

export default function HabitPageHeader() {
  const { selectedHabit } = useHabitStore();

  if (!selectedHabit) {
    return (
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">Habit</h1>
        <p className="text-gray-600 dark:text-gray-400">No habit selected</p>
      </div>
    );
  }

  return (
    <div className="mb-6">
      <div className="flex items-center gap-3 mb-2">
        {selectedHabit.color && (
          <div 
            className="w-4 h-4 rounded-full flex-shrink-0"
            style={{ backgroundColor: selectedHabit.color }}
          />
        )}
        <h1 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
          {selectedHabit.title}
        </h1>
      </div>
      
      {selectedHabit.description && (
        <p className="text-gray-600 dark:text-gray-400 mb-3">
          {selectedHabit.description}
        </p>
      )}
      
      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
        <span className="inline-flex items-center px-2 py-1 rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
          {selectedHabit.category}
        </span>
        <span>Target: {selectedHabit.target}</span>
        <span>•</span>
        <span className="capitalize">{selectedHabit.frequency}</span>
      </div>
    </div>
  );
}
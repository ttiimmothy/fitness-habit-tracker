import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import toast from 'react-hot-toast';
import { createHabitSchema, CreateHabitFormData } from '../../schemas/habitSchemas';
import { useUpdateHabit } from '../../hooks/useHabits';

interface UpdateHabitFormProps {
  habit: {
    id: string;
    title: string;
    description?: string;
    category: string;
    frequency: string;
    target: number;
    color?: string;
  };
  onSuccess?: () => void;
}

const frequencyOptions = [
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
];

const colorOptions = [
  { value: '#3B82F6', label: 'Blue' },
  { value: '#10B981', label: 'Green' },
  { value: '#F59E0B', label: 'Yellow' },
  { value: '#EF4444', label: 'Red' },
  { value: '#8B5CF6', label: 'Purple' },
  { value: '#F97316', label: 'Orange' },
  { value: '#06B6D4', label: 'Cyan' },
  { value: '#84CC16', label: 'Lime' },
];

const categoryOptions = [
  { value: 'fitness', label: 'Fitness' },
  { value: 'health', label: 'Health' },
  { value: 'productivity', label: 'Productivity' },
  { value: 'learning', label: 'Learning' },
  { value: 'mindfulness', label: 'Mindfulness' },
  { value: 'social', label: 'Social' },
  { value: 'creative', label: 'Creative' },
  { value: 'other', label: 'Other' },
];

export default function UpdateHabitForm({ habit, onSuccess }: UpdateHabitFormProps) {
  const updateHabitMutation = useUpdateHabit();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CreateHabitFormData>({
    resolver: zodResolver(createHabitSchema),
    defaultValues: {
      title: habit.title,
      description: habit.description || '',
      category: habit.category,
      frequency: habit.frequency as 'daily' | 'weekly' | 'monthly',
      target: habit.target,
      // color: habit.color || '#3B82F6',
    },
  });

  // Reset form when habit changes
  useEffect(() => {
    reset({
      title: habit.title,
      description: habit.description || '',
      category: habit.category,
      frequency: habit.frequency as 'daily' | 'weekly' | 'monthly',
      target: habit.target,
      // color: habit.color || '#3B82F6',
    });
  }, [habit, reset]);

  const onSubmit = async (data: CreateHabitFormData) => {
    try {
      await updateHabitMutation.mutateAsync({
        id: habit.id,
        data,
      });
      toast.success('Habit updated successfully!');
      onSuccess?.();
    } catch (error: any) {
      toast.error(error?.response?.data?.message || error?.message || 'Failed to update habit');
      console.error('Failed to update habit:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Title *
            </label>
            <input
              {...register('title')}
              type="text"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 bg-white dark:text-white"
              placeholder="Enter habit title"
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.title.message}
              </p>
            )}
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Description
            </label>
            <textarea
              {...register('description')}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 bg-white dark:text-white"
              placeholder="Enter habit description (optional)"
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.description.message}
              </p>
            )}
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Category *
            </label>
            <select
              {...register('category')}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 bg-white dark:text-white"
            >
              {categoryOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {errors.category && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.category.message}
              </p>
            )}
          </div>

          {/* Frequency */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Frequency *
            </label>
            <select
              {...register('frequency')}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 bg-white dark:text-white"
            >
              {frequencyOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {errors.frequency && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.frequency.message}
              </p>
            )}
          </div>

          {/* Target */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Target (times per {habit.frequency}) *
            </label>
            <input
              {...register('target', { valueAsNumber: true })}
              type="number"
              min="1"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 bg-white dark:text-white"
              placeholder="Enter target number"
            />
            {errors.target && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.target.message}
              </p>
            )}
          </div>

          {/* Color */}
          {/* <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Color
            </label>
            <div className="grid grid-cols-4 gap-2">
              {colorOptions.map((option) => (
                <label key={option.value} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    {...register('color')}
                    type="radio"
                    value={option.value}
                    className="sr-only"
                  />
                  <div
                    className={`w-8 h-8 rounded-full border-2 ${
                      option.value === (habit.color || '#3B82F6')
                        ? 'border-gray-900 dark:border-gray-100'
                        : 'border-gray-300 dark:border-gray-600'
                    }`}
                    style={{ backgroundColor: option.value }}
                  />
                  <span className="text-xs text-gray-600 dark:text-gray-400">
                    {option.label}
                  </span>
                </label>
              ))}
            </div>
            {errors.color && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.color.message}
              </p>
            )}
          </div> */}

      {/* Submit Button */}
      <div className="flex justify-end pt-4">
        <button
          type="submit"
          disabled={updateHabitMutation.isPending}
          className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {updateHabitMutation.isPending ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Updating...
            </>
          ) : (
            'Update Habit'
          )}
        </button>
      </div>
    </form>
  );
}

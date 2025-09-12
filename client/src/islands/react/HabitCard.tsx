import { useState } from 'react';
import { useHabits, useDeleteHabit } from '../../hooks/useHabits';
import { useHabitStore } from '../../store/habitStore';
import AddHabitButton from './AddHabitButton';
import {useLogHabit, useTodayHabitLogs} from "../../hooks/useHabitLog";
import { Trash2, Edit } from 'lucide-react';
import UpdateHabitSidebar from './UpdateHabitSidebar';
import toast from 'react-hot-toast';

export default function HabitCard() {
  const { data: habits, isLoading, error } = useHabits();
  const { data: todayLogs, isLoading: todayLogsLoading } = useTodayHabitLogs();
  const logHabitMutation = useLogHabit();
  const deleteHabitMutation = useDeleteHabit();
  const [loggingHabits, setLoggingHabits] = useState<Set<string>>(new Set());
  const [showQuantitySelector, setShowQuantitySelector] = useState<Set<string>>(new Set());
  const [selectedQuantities, setSelectedQuantities] = useState<Record<string, number>>({});
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<string | null>(null);
  const [showUpdateForm, setShowUpdateForm] = useState<string | null>(null);
  const { setSelectedHabit } = useHabitStore();

  const handleQuickLog = async (e: React.MouseEvent, habitId: string, quantity: number = 1) => {
    e.preventDefault();
    
    // Add habit to logging set
    setLoggingHabits(prev => new Set(prev).add(habitId));
    
    try {
      await logHabitMutation.mutateAsync({ id: habitId, quantity });
    } catch (error) {
      console.error('Failed to log habit:', error);
    } finally {
      // Remove habit from logging set
      setLoggingHabits(prev => {
        const newSet = new Set(prev);
        newSet.delete(habitId);
        return newSet;
      });
      // Hide quantity selector
      setShowQuantitySelector(prev => {
        const newSet = new Set(prev);
        newSet.delete(habitId);
        return newSet;
      });
    }
  };

  const handleQuantitySelect = (habitId: string, quantity: number) => {
    setSelectedQuantities(prev => ({
      ...prev,
      [habitId]: quantity
    }));
  };

  const toggleQuantitySelector = (e: React.MouseEvent, habitId: string) => {
    e.preventDefault();
    e.stopPropagation();
    
    setShowQuantitySelector(prev => {
      const newSet = new Set(prev);
      if (newSet.has(habitId)) {
        newSet.delete(habitId);
      } else {
        newSet.add(habitId);
      }
      return newSet;
    });
  };

  const handleHabitClick = (habit: any) => {
    setSelectedHabit(habit);
  };

  const handleDeleteHabit = async (habitId: string) => {
    try {
      await deleteHabitMutation.mutateAsync(habitId);
      toast.success('Habit deleted successfully!');
      setShowDeleteConfirm(null);
    } catch (error: any) {
      toast.error(error?.response?.data?.message || error?.message || 'Failed to delete habit');
      console.error('Failed to delete habit:', error);
    }
  };

  const handleUpdateClose = () => {
    setShowUpdateForm(null);
  };

  // Helper function to get habit progress for today
  const getHabitProgress = (habitId: string) => {
    if (!todayLogs) return { current: 0, target: 1, isComplete: false };
    const todayLog = todayLogs.find(log => log.habit_id === habitId);
    if (!todayLog) return { current: 0, target: 1, isComplete: false };
    
    return {
      current: todayLog.current_progress || 0,
      target: todayLog.target,
      isComplete: todayLog.current_progress >= todayLog.target
    };
  };

  // Helper function to check if a habit is already logged today
  const isHabitLoggedToday = (habitId: string) => {
    const progress = getHabitProgress(habitId);
    return progress.isComplete;
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
      {habits?.map((habit) => {
        const progress = getHabitProgress(habit.id);
        const showQuantity = showQuantitySelector.has(habit.id);
        const isComplete = progress.isComplete;
        const canLogMore = progress.current < progress.target;
        
        return (
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
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-2 h-5">
                  {habit.description ?? ""}
                </div>
                {/* Category Badge */}
                <div className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                  {habit.category}
                </div>
              </div>
              {/* Action Buttons */}
              <div className="flex items-center gap-1">
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    setShowUpdateForm(habit.id);
                  }}
                  className="p-1 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  title="Edit habit"
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    setShowDeleteConfirm(habit.id);
                  }}
                  className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                  title="Delete habit"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
              <span className="capitalize">{habit.frequency}</span>
              <span>Target: {habit.target}</span>
            </div>

            {/* Progress Bar for habits with target >= 1 */}
            {(
              <div className="mt-2">
                <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400 mb-1">
                  <span>Progress: {progress.current}/{progress.target}</span>
                  <span className={isComplete ? 'text-green-600 dark:text-green-400' : ''}>
                    {isComplete ? '✓ Complete' : `${progress.target - progress.current} remaining`}
                  </span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${Math.min((progress.current / progress.target) * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
            )}
            
            {/* Quick Log Button */}
            <div className="mt-2 flex gap-2">
              {habit.target > 1 && canLogMore && !isComplete ? (
                <>
                  <button 
                    onClick={(e) => toggleQuantitySelector(e, habit.id)}
                    className="flex-1 inline-flex items-center justify-center rounded px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white transition-colors"
                  >
                    {showQuantity ? 'Cancel' : 'Log Progress'}
                  </button>
                  
                  {showQuantity && (
                    <div className="flex gap-1">
                      {(() => {
                        const remaining = progress.target - progress.current;
                        const quantities:number[] = [];
                        
                        // Always show +1
                        quantities.push(1);
                        
                        // Add +2 if there's room
                        if (remaining >= 2) quantities.push(2);
                        
                        // Add +3 if there's room
                        if (remaining >= 3) quantities.push(3);
                        
                        // Add "Complete" button if remaining is 4 or more
                        if (remaining >= 4) quantities.push(remaining);
                        
                        return quantities.map(qty => (
                          <button
                            key={qty}
                            onClick={(e) => handleQuickLog(e, habit.id, qty)}
                            disabled={loggingHabits.has(habit.id)}
                            className={`px-2 py-1 text-xs rounded transition-colors ${
                              loggingHabits.has(habit.id)
                                ? 'bg-gray-400 text-white cursor-not-allowed'
                                : qty === remaining
                                ? 'bg-blue-600 hover:bg-blue-700 text-white font-medium'
                                : 'bg-green-600 hover:bg-green-700 text-white'
                            }`}
                          >
                            {qty === remaining ? 'Complete' : `+${qty}`}
                          </button>
                        ));
                      })()}
                    </div>
                  )}
                </>
              ) : (
                <button 
                  onClick={(e) => handleQuickLog(e, habit.id)}
                  disabled={loggingHabits.has(habit.id) || isComplete}
                  className={`w-full inline-flex items-center justify-center rounded px-3 py-1 text-sm transition-colors ${
                    isComplete
                      ? 'bg-gray-500 text-white cursor-not-allowed'
                      : loggingHabits.has(habit.id)
                      ? 'bg-green-400 text-white cursor-not-allowed'
                      : 'bg-green-600 hover:bg-green-700 text-white'
                  }`}
                >
                  {isComplete 
                    ? '✓ Complete' 
                    : loggingHabits.has(habit.id) 
                    ? 'Logging...' 
                    : 'Quick Log'
                  }
          </button>
              )}
            </div>
          </a>
        );
      })}
      
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

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md mx-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Delete Habit
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Are you sure you want to delete this habit? This action cannot be undone and will remove all associated progress data.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="flex-1 px-4 py-2 text-sm bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDeleteHabit(showDeleteConfirm)}
                disabled={deleteHabitMutation.isPending}
                className="flex-1 px-4 py-2 text-sm bg-red-600 hover:bg-red-700 text-white rounded transition-colors disabled:bg-red-400 disabled:cursor-not-allowed"
              >
                {deleteHabitMutation.isPending ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Update Habit Sidebar */}
      {showUpdateForm && habits && (
        <UpdateHabitSidebar
          habit={habits.find(h => h.id === showUpdateForm)!}
          isOpen={!!showUpdateForm}
          onClose={handleUpdateClose}
        />
      )}
    </>
  );
}



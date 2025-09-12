import { useState } from 'react';
import { useHabitStore } from '../../store/habitStore';
import { useLogHabit } from '../../hooks/useHabitLog';
import { useDeleteHabit } from '../../hooks/useHabits';
import UpdateHabitSidebar from './UpdateHabitSidebar';
import { Edit } from 'lucide-react';
import toast from 'react-hot-toast';
import {useTodayHabitLogsStats} from "@/hooks/useStats";

export default function IndividualHabitQuickLog() {
  const { selectedHabit, clearSelectedHabit } = useHabitStore();
  const { data: todayLogs, isLoading: todayLogsLoading } = useTodayHabitLogsStats();
  const logHabitMutation = useLogHabit();
  const deleteHabitMutation = useDeleteHabit();
  const [isLogging, setIsLogging] = useState(false);
  const [showQuantitySelector, setShowQuantitySelector] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [showUpdateForm, setShowUpdateForm] = useState(false);

  // Helper function to get habit progress for today
  const getHabitProgress = (habitId: string) => {
    if (!todayLogs || !habitId) return { current: 0, target: 1, isComplete: false };
    const todayLog = todayLogs.find(log => log.habit_id === habitId);
    if (!todayLog) return { current: 0, target: 1, isComplete: false };
    
    return {
      current: todayLog.current_progress || 0,
      target: todayLog.target,
      isComplete: (todayLog.current_progress || 0) >= todayLog.target
    };
  };

  const handleQuickLog = async (quantity: number = 1) => {
    if (!selectedHabit) return;
    
    setIsLogging(true);
    
    try {
      await logHabitMutation.mutateAsync({ id: selectedHabit.id, quantity });
    } catch (error) {
      console.error('Failed to log habit:', error);
    } finally {
      setIsLogging(false);
      setShowQuantitySelector(false);
    }
  };

  const toggleQuantitySelector = () => {
    setShowQuantitySelector(prev => !prev);
  };

  const handleDeleteHabit = async () => {
    if (!selectedHabit) return;
    
    try {
      await deleteHabitMutation.mutateAsync(selectedHabit.id);
      toast.success('Habit deleted successfully!');
      clearSelectedHabit();
      // Redirect to dashboard after successful deletion
      window.location.href = '/';
    } catch (error: any) {
      toast.error(error?.response?.data?.message || error?.message || 'Failed to delete habit');
      console.error('Failed to delete habit:', error);
    }
  };

  const handleUpdateClose = () => {
    setShowUpdateForm(false);
  };

  if (!selectedHabit) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <p className="text-gray-500 dark:text-gray-400">No habit selected</p>
      </div>
    );
  }

  if (todayLogsLoading) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
        </div>
      </div>
    );
  }

  const progress = getHabitProgress(selectedHabit.id);
  const isComplete = progress.isComplete;
  const canLogMore = progress.current < progress.target;

  return (
    <div className="p-4 border rounded bg-white dark:bg-neutral-900 max-w-3xl mx-auto">
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Today's Progress
          </h3>
          <button
            onClick={() => setShowUpdateForm(true)}
            className="p-1 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            title="Edit habit"
          >
            <Edit className="w-4 h-4" />
          </button>
        </div>
        
        {/* Progress Bar for habits with target > 1 */}
        {selectedHabit.target > 1 && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
              <span>Progress: {progress.current}/{progress.target}</span>
              <span className={isComplete ? 'text-green-600 dark:text-green-400 font-medium' : ''}>
                {isComplete ? '✓ Complete' : `${progress.target - progress.current} remaining`}
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <div 
                className="bg-green-600 h-3 rounded-full transition-all duration-300"
                style={{ width: `${Math.min((progress.current / progress.target) * 100, 100)}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Simple progress display for target = 1 */}
        {selectedHabit.target === 1 && (
          <div className="mb-4">
            <div className={`text-sm font-medium ${isComplete ? 'text-green-600 dark:text-green-400' : 'text-gray-600 dark:text-gray-400'}`}>
              {isComplete ? '✓ Completed today' : 'Not completed today'}
            </div>
          </div>
        )}
      </div>

      {/* Quick Log Section */}
      <div className="space-y-3">
        {selectedHabit.target > 1 && canLogMore && !isComplete ? (
          <>
            <button 
              onClick={toggleQuantitySelector}
              className="w-full inline-flex items-center justify-center rounded px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white transition-colors"
            >
              {showQuantitySelector ? 'Cancel' : 'Log Progress'}
            </button>
            
            {showQuantitySelector && (
              <div className="space-y-2">
                <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
                  How much progress did you make?
                </p>
                <div className="flex gap-2 justify-center">
                  {(() => {
                    const remaining = progress.target - progress.current;
                    const quantities: number[] = [];
                    
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
                        onClick={() => handleQuickLog(qty)}
                        disabled={isLogging}
                        className={`px-3 py-2 text-sm rounded transition-colors ${
                          isLogging
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
            </div>
          )}
        </>
      ) : (
        <button 
          onClick={() => handleQuickLog()}
          disabled={isLogging || isComplete}
          className={`w-full inline-flex items-center justify-center rounded px-4 py-2 text-sm transition-colors ${
            isComplete
              ? 'bg-gray-500 text-white cursor-not-allowed'
              : isLogging
              ? 'bg-green-400 text-white cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-700 text-white'
          }`}
        >
          {isComplete 
            ? '✓ Complete' 
            : isLogging 
            ? 'Logging...' 
            : 'Quick Log'
          }
        </button>
      )}
    </div>

    {/* Delete Habit Section */}
    <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
      <div className="text-sm text-gray-600 dark:text-gray-400 mb-3">
        Danger Zone
      </div>
      <button
        onClick={() => setShowDeleteConfirm(true)}
        disabled={deleteHabitMutation.isPending}
        className="w-full inline-flex items-center justify-center rounded px-4 py-2 text-sm bg-red-600 hover:bg-red-700 text-white transition-colors disabled:bg-red-400 disabled:cursor-not-allowed"
      >
        {deleteHabitMutation.isPending ? 'Deleting...' : 'Delete Habit'}
      </button>
    </div>

    {/* Delete Confirmation Modal */}
    {showDeleteConfirm && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md mx-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            Delete Habit
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Are you sure you want to delete "{selectedHabit?.title}"? This action cannot be undone and will remove all associated progress data.
          </p>
          <div className="flex gap-3">
            <button
              onClick={() => setShowDeleteConfirm(false)}
              className="flex-1 px-4 py-2 text-sm bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleDeleteHabit}
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
    {selectedHabit && (
      <UpdateHabitSidebar
        habit={selectedHabit}
        isOpen={showUpdateForm}
        onClose={handleUpdateClose}
      />
    )}
  </div>
);
}

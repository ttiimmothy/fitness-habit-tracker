import { useHabits } from '../../hooks/useHabits';
import { useMultipleHabitsStats } from '../../hooks/useStats';

export const StreakCounter = () => {
  const { data: habits, isLoading: habitsLoading, error: habitsError } = useHabits();
  const habitIds = habits?.map(habit => habit.id) || [];
  const { data: habitsStats, isLoading: statsLoading, error: statsError } = useMultipleHabitsStats(habitIds);

  if (habitsLoading || statsLoading) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (habitsError || statsError) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="text-sm text-red-600 dark:text-red-400">
          Failed to load streak data
        </div>
      </div>
    );
  }

  if (!habits || habits.length === 0) {
    return (
      <div className="p-4 border rounded bg-white dark:bg-neutral-900">
        <div className="text-sm text-gray-500 dark:text-gray-400">
          No habits to track streaks
        </div>
      </div>
    );
  }

  // Calculate total current streak across all habits
  const totalCurrentStreak = habitsStats ? Object.values(habitsStats).reduce((sum, stats) => sum + stats.current_streak, 0) : 0;

  return (
    <div className="p-4 border rounded bg-white dark:bg-neutral-900">
      {/* <div className="mb-4">
        <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Streak</div>
        <div className="text-3xl font-semibold text-gray-900 dark:text-gray-100">
          🔥 {totalCurrentStreak} days
        </div>
      </div> */}
      
      <div className="space-y-3">
        <div className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
        🔥 Streaks
        </div>
        
        {habits.map((habit) => {
          const stats = habitsStats?.[habit.id];
          const currentStreak = stats?.current_streak || 0;
          const longestStreak = stats?.longest_streak || 0;
          const completionRate = stats?.completion_rate || 0;
          
          return (
            <div key={habit.id} className="flex items-center justify-between py-2 px-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                  {habit.title}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  {habit.category}
                </div>
              </div>
              
              <div className="flex items-center gap-3 text-sm">
                <div className="text-center">
                  <div className="font-semibold text-green-600 dark:text-green-400">
                    {currentStreak}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    current
                  </div>
                </div>
                
                <div className="text-gray-300 dark:text-gray-600">|</div>
                
                <div className="text-center">
                  <div className="font-semibold text-blue-600 dark:text-blue-400">
                    {longestStreak}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    best
                  </div>
                </div>
                
                <div className="text-gray-300 dark:text-gray-600">|</div>
                
                <div className="text-center">
                  <div className="font-semibold text-purple-600 dark:text-purple-400">
                    {Math.round(completionRate)}%
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    completion
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}



import { useEffect, useState } from 'react';
import { useAuthStore } from '../../store/authStore';
// import { useLogout } from '../../hooks/useAuth';
import { useHabits } from '../../hooks/useHabits';
import { useMultipleHabitsStats } from '../../hooks/useStats';
// import PasswordUpdateForm from './PasswordUpdateForm';
// import UpdateUsernameSidebar from './UpdateUsernameSidebar';
// import { XLargeAvatar } from '../../components/Avatar';

export const UserProfile = () => {
  const { user } = useAuthStore();
  // const logoutMutation = useLogout();
  const [isLoaded, setIsLoaded] = useState(false);
  // const [isPasswordSidebarOpen, setIsPasswordSidebarOpen] = useState(false);
  // const [isUsernameSidebarOpen, setIsUsernameSidebarOpen] = useState(false);
  
  // Fetch habits and stats data
  const { data: habits, isLoading: habitsLoading } = useHabits();
  const { data: habitsStats, isLoading: statsLoading } = useMultipleHabitsStats(habits?.map(h => h.id) || []);

  // Calculate stats
  const activeHabits = habits?.length || 0;
  const currentStreak = habitsStats 
    ? Math.max(...Object.values(habitsStats).map(stat => stat.current_streak), 0)
    : 0;
  const averageCompletionRate = habitsStats && Object.keys(habitsStats).length > 0
    ? Math.round(Object.values(habitsStats).reduce((sum, stat) => sum + stat.completion_rate, 0) / Object.keys(habitsStats).length)
    : 0;

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  // // Handle ESC key to close sidebar
  // useEffect(() => {
  //   const handleEscKey = (event: KeyboardEvent) => {
  //     if (event.key === 'Escape' && (isPasswordSidebarOpen || isUsernameSidebarOpen)) {
  //       if (isPasswordSidebarOpen) closePasswordSidebar();
  //       if (isUsernameSidebarOpen) closeUsernameSidebar();
  //     }
  //   };

  //   if (isPasswordSidebarOpen || isUsernameSidebarOpen) {
  //     document.addEventListener('keydown', handleEscKey);
  //     // Prevent body scroll when sidebar is open
  //     document.body.style.overflow = 'hidden';
  //   }

  //   return () => {
  //     document.removeEventListener('keydown', handleEscKey);
  //     document.body.style.overflow = 'unset';
  //   };
  // }, [isPasswordSidebarOpen, isUsernameSidebarOpen]);

  // const handleLogout = () => {
  //   logoutMutation.mutate(undefined, {
  //     onSuccess: () => {
  //       // The mutation already handles setUser(null) via setAuth(null)
  //       window.location.href = '/login';
  //     },
  //     onError: () => {
  //       // The mutation already handles setUser(null) via setAuth(null)
  //       window.location.href = '/login';
  //     },
  //   });
  // };

  // const openPasswordSidebar = () => {
  //   setIsPasswordSidebarOpen(true);
  // };

  // const closePasswordSidebar = () => {
  //   setIsPasswordSidebarOpen(false);
  // };

  // const openUsernameSidebar = () => {
  //   setIsUsernameSidebarOpen(true);
  // };

  // const closeUsernameSidebar = () => {
  //   setIsUsernameSidebarOpen(false);
  // };

  // // Close sidebar when clicking outside
  // const handleBackdropClick = (e: React.MouseEvent) => {
  //   if (isPasswordSidebarOpen) closePasswordSidebar();
  //   if (isUsernameSidebarOpen) closeUsernameSidebar();
  // };

  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
              Not authenticated
            </h3>
            <div className="mt-2 text-sm text-red-700 dark:text-red-300">
              <p>You need to be logged in to view your profile.</p>
            </div>
            <div className="mt-4">
              <a
                href="/login"
                className="bg-red-100 dark:bg-red-800 text-red-800 dark:text-red-200 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-200 dark:hover:bg-red-700"
              >
                Go to Login
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Main Content Area */}
      <div className="space-y-6">
        {/* User Information Card */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">Profile Information</h2>
          </div>
          <div className="px-6 py-4">
            <div className="flex items-center space-x-4">
              {/* Avatar */}
              <div className="flex-shrink-0">
                {user.avatar_url ? (
                  <img
                    className="h-16 w-16 rounded-full object-cover"
                    src={user.avatar_url}
                    alt={`${user.name || user.email}'s avatar`}
                  />
                ) : (
                  <div className="h-16 w-16 rounded-full bg-blue-500 flex items-center justify-center">
                    <span className="text-white text-xl font-semibold">
                      {(user.name || user.email).charAt(0).toUpperCase()}
                    </span>
                  </div>
                )}
              </div>
              
              {/* User Details */}
              <div className="flex-1 min-w-0">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Username
                    </label>
                    <p className="mt-1 text-sm text-gray-900 dark:text-white font-medium">
                      {user.name || 'Not set'}
                    </p>
                    {!user.name && (
                      <p className="mt-1 text-xs text-amber-600 dark:text-amber-400">
                        Click "Change Username" to set your display name
                      </p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Email Address
                    </label>
                    <p className="mt-1 text-sm text-gray-900 dark:text-white">
                      {user.email}
                    </p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Member Since
                    </label>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                      {new Date().toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Quick Stats Card */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">Quick Stats</h2>
          </div>
          <div className="px-6 py-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {habitsLoading ? '...' : activeHabits}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Active Habits</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {statsLoading ? '...' : currentStreak}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Current Streak</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                  {statsLoading ? '...' : `${averageCompletionRate}%`}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Avg Completion Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

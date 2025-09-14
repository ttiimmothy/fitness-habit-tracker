import {useAuthStore} from "../../store/authStore";
import {useEffect, useState} from "react";
import UpdateUsernameSidebar from "./UpdateUsernameSidebar";
import PasswordUpdateForm from "./PasswordUpdateForm";
import {useLogout} from "../../hooks/useAuth";

export const AccountAction = () => {
  const { user } = useAuthStore();
  const logoutMutation = useLogout();
  
  const [isPasswordSidebarOpen, setIsPasswordSidebarOpen] = useState(false);
  const [isUsernameSidebarOpen, setIsUsernameSidebarOpen] = useState(false);
  // Handle ESC key to close sidebar
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && (isPasswordSidebarOpen || isUsernameSidebarOpen)) {
        if (isPasswordSidebarOpen) closePasswordSidebar();
        if (isUsernameSidebarOpen) closeUsernameSidebar();
      }
    };

    if (isPasswordSidebarOpen || isUsernameSidebarOpen) {
      document.addEventListener('keydown', handleEscKey);
      // Prevent body scroll when sidebar is open
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
      document.body.style.overflow = 'unset';
    };
  }, [isPasswordSidebarOpen, isUsernameSidebarOpen]);

  const handleLogout = () => {
    logoutMutation.mutate(undefined, {
      onSuccess: () => {
        // The mutation already handles setUser(null) via setAuth(null)
        window.location.href = '/login';
      },
      onError: () => {
        // The mutation already handles setUser(null) via setAuth(null)
        window.location.href = '/login';
      },
    });
  };

  const openPasswordSidebar = () => {
    setIsPasswordSidebarOpen(true);
  };

  const closePasswordSidebar = () => {
    setIsPasswordSidebarOpen(false);
  };

  const openUsernameSidebar = () => {
    setIsUsernameSidebarOpen(true);
  };

  const closeUsernameSidebar = () => {
    setIsUsernameSidebarOpen(false);
  };

  // Close sidebar when clicking outside
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (isPasswordSidebarOpen) closePasswordSidebar();
    if (isUsernameSidebarOpen) closeUsernameSidebar();
  };

  return (
    <div>
    {/* Account Actions Card */}
    <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-medium text-gray-900 dark:text-white">Account Actions</h2>
      </div>
      <div className="px-6 py-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={openUsernameSidebar}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg className="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Change Username
          </button>
          
          <button
            onClick={openPasswordSidebar}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg className="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1721 9z" />
            </svg>
            Change Password
          </button>
          
          <button
            onClick={handleLogout}
            disabled={logoutMutation.isPending}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {logoutMutation.isPending ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Logging out...
              </>
            ) : (
              <>
                <svg className="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Sign Out
              </>
            )}
          </button>
        </div>
      </div>
    </div>

    {/* Username Update Sidebar */}
    <UpdateUsernameSidebar 
        isOpen={isUsernameSidebarOpen}
        onClose={closeUsernameSidebar}
        currentName={user?.name || ''}
      />

      {/* Password Update Sidebar Overlay */}
      {isPasswordSidebarOpen && (
        <div 
          className="fixed inset-0 z-50 overflow-hidden"
          
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black bg-opacity-50 transition-opacity" 
            onClick={handleBackdropClick}
          />
          
          {/* Sidebar */}
          <div className="absolute right-0 top-0 h-full w-full max-w-md bg-white dark:bg-gray-800 shadow-xl transform transition-transform">
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-medium text-gray-900 dark:text-white">Update Password</h2>
                <button
                  onClick={closePasswordSidebar}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              {/* Content */}
              <div className="flex-1 overflow-y-auto">
                <div className="p-6">
                  <PasswordUpdateForm onSuccess={closePasswordSidebar} />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
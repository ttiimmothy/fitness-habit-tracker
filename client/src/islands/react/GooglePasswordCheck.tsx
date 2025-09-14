import { useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';

export const GooglePasswordCheck = ({ children }: { children: React.ReactNode }) => {
  const { user } = useAuthStore();

  useEffect(() => {
    // Check if user is from Google OAuth and needs to set up password
    if (user && user.provider === 'google' && !user.has_password) {
      // Redirect to password setup page
      window.location.href = '/setup-password';
    }
  }, [user]);

  // Don't render children if redirecting
  if (user && user.provider === 'google' && !user.has_password) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Redirecting to password setup...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

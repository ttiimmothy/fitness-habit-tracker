import React, { useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';
import { api } from '../../lib/api';

interface AuthCheckProps {
  children: React.ReactNode;
}

export default function AuthCheck({ children }: AuthCheckProps) {
  const { user, setAuth } = useAuthStore();

  useEffect(() => {
    const checkAuth = async () => {
      // If we already have user data, we're good
      if (user) {
        return;
      }

      try {
        // Try to get current user from API
        const response = await api('/auth/me');
        const userData = response.data;
        setAuth(userData.user);
      } catch (error) {
        console.error('Authentication check failed:', error);
        // Redirect to login if authentication fails
        // window.location.href = '/login';
      }
    };

    checkAuth();
  }, [user, setAuth]);

  // Show loading while checking authentication
  // if (!user) {
  //   return (
  //     <div className="flex items-center justify-center min-h-screen">
  //       <div className="text-center">
  //         <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
  //         <p className="text-gray-600 dark:text-gray-400">Checking authentication...</p>
  //       </div>
  //     </div>
  //   );
  // }

  return <main className="p-8 text-center">{children}</main>;
}

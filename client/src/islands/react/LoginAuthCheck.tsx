import React, { useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';
import { api } from '../../lib/api';

export const LoginAuthCheck = ({ children }: {
  children: React.ReactNode;
}) => {
  const { user, setAuth } = useAuthStore();

  useEffect(() => {
    const checkAuth = async () => {
      // If we already have user data, we're good
      if (user) {
        window.location.href = '/';
        return;
      }

      try {
        // Try to get current user from API
        const response = await api('/auth/me');
        const userData = response.data;
        setAuth(userData.user);
        window.location.href = '/';
      } catch (error) {
        console.error('Authentication check failed:', error);
      }
    };

    checkAuth();
  }, [user, setAuth]);

  return <main className="p-8 text-center">{children}</main>;
}

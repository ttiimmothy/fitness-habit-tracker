import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import { useAuthStore, type User } from '../store/authStore';

// Types
interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  name: string;
  email: string;
  password: string;
}

interface AuthResponse {
  accessToken: string;
  user: User;
}

// Query keys
export const authKeys = {
  all: ['auth'] as const,
  user: () => [...authKeys.all, 'user'] as const,
};

// Custom hooks
export function useLogin() {
  const setAuth = useAuthStore((s) => s.setAuth);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (credentials: LoginCredentials): Promise<AuthResponse> => {
      const response = await api.post('/auth/login', credentials);
      return response.data;
    },
    onSuccess: (data) => {
      setAuth(data.user);
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: authKeys.user() });
    },
    onError: (error: any) => {
      console.error('Login failed:', error);
    },
  });
}

export function useRegister() {
  const setAuth = useAuthStore((s) => s.setAuth);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: RegisterData): Promise<AuthResponse> => {
      const response = await api.post('/auth/register', data);
      return response.data;
    },
    onSuccess: (data) => {
      setAuth(data.user);
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: authKeys.user() });
    },
    onError: (error: any) => {
      console.error('Registration failed:', error);
    },
  });
}

export function useUser() {
  const user = useAuthStore((s) => s.user);

  return useQuery({
    queryKey: authKeys.user(),
    queryFn: async (): Promise<User> => {
      const response = await api('/auth/me');
      return response.data.user;
    },
    enabled: !!user, // Only run query if we have a user in store
    initialData: user,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useLogout() {
  const clear = useAuthStore((s) => s.logout);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      // Call logout endpoint to clear server-side cookies
      try {
        await api.post('/auth/logout');
      } catch (error) {
        // Even if logout fails on server, we'll still clear local state
        console.warn('Logout API call failed:', error);
      }
    },
    onSuccess: () => {
      // Clear local state
      clear();
      // Clear all cached data
      queryClient.clear();
    },
    onError: () => {
      // Clear local state even if API call fails
      clear();
      queryClient.clear();
    },
  });
}

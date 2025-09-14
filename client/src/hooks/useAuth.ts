import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import toast from 'react-hot-toast';
import {validateOAuthConfig, getGoogleRedirectUri} from "../config/oauth";
import {useAuthStore, User} from "../store/authStore";

// interface GoogleAuthResponse {
//   user: {
//     id: string;
//     name: string;
//     email: string;
//   };
// }
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

interface UpdateProfileData {
  name: string;
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
  const {setAuth} = useAuthStore();
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
      // Clear user state
      setAuth(null);
      // Clear all cached data
      queryClient.clear();
    },
    onError: () => {
      // Clear user state even if API call fails
      setAuth(null);
      queryClient.clear();
    },
  });
}

export function useUpdateProfile() {
  const {user, setAuth} = useAuthStore();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: UpdateProfileData) => {
      const response = await api.put('/auth/update-profile', data);
      return response.data;
    },
    onSuccess: (data) => {
      // Update the user in the store with the new name
      const newUser = {...user as User, name: data.name}
      setAuth(newUser)
      // setAuth((prev: User) => prev ? {...prev, name:data.name} : null)
      // const currentUser = useAuthStore.getState().user;
      // if (currentUser) {
      //   setAuth({ ...currentUser, name: data.name });
      // }
      // Invalidate user query to refetch updated data
      queryClient.invalidateQueries({ queryKey: authKeys.user() });
    },
  });
}

// export function useGoogleLogin() {
//   const {setAuth} = useAuthStore();
//   const queryClient = useQueryClient();

//   return useMutation({
//     mutationFn: async (code: string) => {
//       const response = await api.post('/auth/google', { code });
//       return response.data
//     },
//     onSuccess: (data) => {
//       // Set user data in store
//       setAuth(data.user);
      
//       // Invalidate and refetch user data
//       queryClient.invalidateQueries({ queryKey: authKeys.user() });
      
//       toast.success('Successfully logged in with Google!');
//     },
//     onError: (error: any) => {
//       toast.error(error?.response?.data?.message || error?.message || 'Google login failed');
//     },
//   });
// }

export function useGoogleAuth() {
  // const googleLoginMutation = useGoogleLogin();

  const loginWithGoogle = () => {
    // Redirect to Google OAuth
    window.location.href = getGoogleAuthUrl();
  };

  // const handleGoogleCallback = async (code: string) => {
  //   try {
  //     await googleLoginMutation.mutateAsync(code);
  //     // Redirect to dashboard after successful login
  //     window.location.href = '/';
  //   } catch (error) {
  //     console.error('Google login error:', error);
  //   }
  // };

  return {
    loginWithGoogle,
    // handleGoogleCallback,
    // isLoading: googleLoginMutation.isPending,
    // error: googleLoginMutation.error,
  };
}

// Helper function to get Google auth URL
const getGoogleAuthUrl = () => {
  const GOOGLE_CLIENT_ID = import.meta.env.PUBLIC_GOOGLE_CLIENT_ID || '';
  const redirectUri = getGoogleRedirectUri();
  
  if (!GOOGLE_CLIENT_ID || !validateOAuthConfig()) {
    throw new Error('Google OAuth Client ID not configured');
  }
  
  const params = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: redirectUri,
    scope: 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    response_type: 'code',
    access_type: 'offline',
    prompt: 'consent',
  });

  return `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
};

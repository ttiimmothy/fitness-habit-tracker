import React, {useEffect} from 'react'
import {useAuthStore} from "../../store/authStore";
import {api} from "../../lib/api";

const IndexAuthGuard = () => {
  console.log('IndexAuthGuard: Component rendering...');
  
  const {setAuth} = useAuthStore()
  
  useEffect(() => {
    console.log('IndexAuthGuard: useEffect running...');
    const checkAuth = async () => {
      try {
        try {
          // Call the /me API to verify authentication (token is in cookies)
          const response = await api("/auth/me");
          const userData = response.data;
          console.log
          // Update auth store with user data
          setAuth(userData.user);
          
          // Redirect to dashboard
          window.location.href = '/dashboard';
        } catch (e) {
          console.error('Failed to verify authentication:', e);
          // Clear auth state and redirect to login
          setAuth(null);
          window.location.href = '/login';
        }
      } catch (e) {
        console.error('Auth check failed:', e);
        window.location.href = '/login';
      }
    }
    
    // Run the auth check when the page loads
    checkAuth();
  }, [setAuth]); // Fixed syntax error

  return <main className="p-8 text-center">Redirecting…</main>
}

export default IndexAuthGuard
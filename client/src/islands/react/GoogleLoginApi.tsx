import {useEffect} from "react";
import {api} from "../../lib/api"
import {useAuthStore} from "../../store/authStore"

export const GoogleLoginApi = ({children}: {children: React.ReactNode}) => {
  const {setAuth} = useAuthStore()

  useEffect(() => {
    // Handle Google OAuth callback
    const callbackGoogleOAuth = async () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        const error = urlParams.get('error');

        // console.log('OAuth callback - code:', code);
        // console.log('OAuth callback - error:', error);

        if (error) {
          console.error('Google OAuth error:', error);
          window.location.href = '/login?error=google_auth_failed';
          return;
        }

        if (!code) {
          console.error('No authorization code received');
          window.location.href = '/login?error=no_code';
          return;
        }

        // Send code to backend
        const response = await api.post('/auth/google', { code })

        if (response.status < 200 || response.status >= 300) {
          const errorData = response.data;
          throw new Error(errorData.message || 'Google authentication failed');
        }

        const data = response.data;
        
        // Store auth data
        // localStorage.setItem('user_data', JSON.stringify(data.user));
        setAuth(data.user)
        console.log(data.user)
        
        // Check if user is from Google OAuth and needs to set up password
        if (data.user.provider === 'google' && !data.user.has_password) {
          // Redirect to password setup page
          window.location.href = '/setup-password';
        } else {
          // Redirect to dashboard
          window.location.href = '/';
        }
        
      } catch (error) {
        console.error('Google auth error:', error);
        window.location.href = '/login?error=google_auth_failed';
      }
    };

    callbackGoogleOAuth()
  }, [setAuth])
 

  return (
    <>{children}</>
  )
}
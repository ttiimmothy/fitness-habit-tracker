import { useEffect } from 'react';
import toast from 'react-hot-toast';

export const LoginErrorHandler = () => {
  useEffect(() => {
    // Check for error parameters in URL
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');
    
    if (error) {
      let errorMessage = '';
      
      switch (error) {
        case 'google_auth_failed':
          errorMessage = 'Google authentication failed. Please try again.';
          break;
        case 'no_code':
          errorMessage = 'No authorization code received from Google. Please try again.';
          break;
        case 'access_denied':
          errorMessage = 'Google login was cancelled. Please try again if you want to sign in.';
          break;
        case 'invalid_request':
          errorMessage = 'Invalid Google OAuth request. Please try again.';
          break;
        case 'unauthorized_client':
          errorMessage = 'Google OAuth client is not authorized. Please contact support.';
          break;
        case 'unsupported_response_type':
          errorMessage = 'Unsupported response type. Please contact support.';
          break;
        case 'invalid_scope':
          errorMessage = 'Invalid OAuth scope. Please contact support.';
          break;
        case 'server_error':
          errorMessage = 'Google server error. Please try again later.';
          break;
        case 'temporarily_unavailable':
          errorMessage = 'Google OAuth is temporarily unavailable. Please try again later.';
          break;
        default:
          errorMessage = `Authentication error: ${error}`;
      }
      
      // Show error toast
      toast.error(errorMessage);
      
      // Clean up URL by removing error parameter
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.delete('error');
      window.history.replaceState({}, '', newUrl.toString());
    }
  }, []);

  return null; // This component doesn't render anything
}

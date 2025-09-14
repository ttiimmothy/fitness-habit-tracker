// OAuth Configuration
export const OAUTH_CONFIG = {
  google: {
    clientId: import.meta.env.PUBLIC_GOOGLE_CLIENT_ID || '',
    scope: 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
  },
};

// Get redirect URI dynamically (only when called on client-side)
export const getGoogleRedirectUri = () => {
  if (typeof window === 'undefined') {
    return '/auth/google/callback'; // Fallback for SSR
  }
  return `${window.location.origin}/auth/google/callback`;
};

// Environment variables validation
export const validateOAuthConfig = () => {
  if (!OAUTH_CONFIG.google.clientId) {
    console.warn('Google OAuth Client ID not configured. Please set PUBLIC_GOOGLE_CLIENT_ID environment variable.');
    return false;
  }
  return true;
};

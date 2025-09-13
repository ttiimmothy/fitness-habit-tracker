// Google OAuth configuration
export const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || '';

// Google OAuth scopes
export const GOOGLE_SCOPES = [
  'https://www.googleapis.com/auth/userinfo.email',
  'https://www.googleapis.com/auth/userinfo.profile',
];

// Google OAuth configuration object
export const GOOGLE_CONFIG = {
  client_id: GOOGLE_CLIENT_ID,
  scope: GOOGLE_SCOPES.join(' '),
  response_type: 'code',
  redirect_uri: `${window.location.origin}/auth/google/callback`,
};

// Generate Google OAuth URL
export const getGoogleAuthUrl = () => {
  const params = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: GOOGLE_CONFIG.redirect_uri,
    scope: GOOGLE_CONFIG.scope,
    response_type: 'code',
    access_type: 'offline',
    prompt: 'consent',
  });

  return `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
};

// Handle Google OAuth callback
export const handleGoogleCallback = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  const error = urlParams.get('error');

  if (error) {
    throw new Error(`Google OAuth error: ${error}`);
  }

  if (!code) {
    throw new Error('No authorization code received from Google');
  }

  return code;
};

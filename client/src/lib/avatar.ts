/**
 * Get avatar URL with fallback to default avatar
 * @param googleImageUrl - Google profile image URL
 * @returns Avatar URL or default avatar path
 */
export const getAvatarUrl = (googleImageUrl: string | null | undefined): string => {
  if (!googleImageUrl) {
    return '/default-avatar.svg';
  }
  
  // For now, return the Google image URL directly
  // TODO: Implement backend proxy to avoid CORS issues
  return googleImageUrl;
};

/**
 * Get avatar URL with error handling
 * @param googleImageUrl - Google profile image URL
 * @param hasError - Whether the image failed to load
 * @returns Avatar URL or default avatar path
 */
export const getAvatarUrlWithFallback = (
  googleImageUrl: string | null | undefined, 
  hasError: boolean = false
): string => {
  if (hasError || !googleImageUrl) {
    return '/default-avatar.svg';
  }
  
  return googleImageUrl;
};

/**
 * Default avatar configuration
 */
export const AVATAR_CONFIG = {
  default: '/default-avatar.svg',
  size: {
    small: 'w-8 h-8',
    medium: 'w-10 h-10',
    large: 'w-12 h-12',
    xlarge: 'w-16 h-16',
  },
  className: 'rounded-full object-cover',
} as const;

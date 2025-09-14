import React, { useState, useEffect } from 'react';
import { getAvatarUrlWithFallback, AVATAR_CONFIG } from '../lib/avatar';

interface AvatarProps {
  src?: string | null;
  alt?: string;
  size?: 'small' | 'medium' | 'large' | 'xlarge';
  className?: string;
  fallback?: string;
}

export default function Avatar({ 
  src, 
  alt = 'User Avatar', 
  size = 'medium',
  className = '',
  fallback
}: AvatarProps) {
  const [hasError, setHasError] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  
  useEffect(() => {
    // Check for dark mode
    const checkDarkMode = () => {
      setIsDarkMode(document.documentElement.classList.contains('dark'));
    };
    
    checkDarkMode();
    
    // Watch for dark mode changes
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });
    
    return () => observer.disconnect();
  }, []);
  
  const getDefaultAvatar = () => {
    return isDarkMode ? '/default-avatar-dark.svg' : '/default-avatar.svg';
  };
  
  const avatarUrl = hasError || !src ? getDefaultAvatar() : src;
  const sizeClass = AVATAR_CONFIG.size[size];
  const baseClass = AVATAR_CONFIG.className;
  
  const handleError = () => {
    setHasError(true);
  };
  
  return (
    <img
      src={avatarUrl}
      alt={alt}
      onError={handleError}
      className={`${sizeClass} ${baseClass} ${className}`}
    />
  );
}

// Convenience components for different sizes
export const SmallAvatar = (props: Omit<AvatarProps, 'size'>) => (
  <Avatar {...props} size="small" />
);

export const MediumAvatar = (props: Omit<AvatarProps, 'size'>) => (
  <Avatar {...props} size="medium" />
);

export const LargeAvatar = (props: Omit<AvatarProps, 'size'>) => (
  <Avatar {...props} size="large" />
);

export const XLargeAvatar = (props: Omit<AvatarProps, 'size'>) => (
  <Avatar {...props} size="xlarge" />
);

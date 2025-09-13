import { Avatar } from '../components/Avatar';

export const AvatarIsland = ({ 
  src, 
  alt = 'User Avatar', 
  size = 'medium',
  className = ''
}: {
  src?: string | null;
  alt?: string;
  size?: 'small' | 'medium' | 'large' | 'xlarge';
  className?: string;
}) => {
  return (
    <Avatar
      src={src}
      alt={alt}
      size={size}
      className={className}
    />
  );
};

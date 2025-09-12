import { useEffect, useState } from 'react';
import { useAuthStore } from '../../store/authStore';

export default function UserMenu() {
  const { user } = useAuthStore();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  if (!isLoaded) {
    return <div className="text-sm opacity-70">Loading...</div>;
  }

  return (
    <div className="flex items-center gap-3">
      {user ? (
        <>
          <a
            href="/user"
            className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
          >
            Profile
          </a>
        </>
      ) : (
        <a
          href="/login"
          className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
        >
          Login
        </a>
      )}
    </div>
  );
}
import React from 'react';
import { PersistQueryProvider } from './react/PersistQueryProvider';
import AuthGuard from './react/AuthGuard';

interface IndexAuthGuardIslandProps {
  children: React.ReactNode;
}

export default function IndexAuthGuardIsland({ children }: IndexAuthGuardIslandProps) {
  return (
    <PersistQueryProvider>
      <AuthGuard>
        {children}
      </AuthGuard>
    </PersistQueryProvider>
  );
}

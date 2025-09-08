import React, { ReactNode, useMemo } from 'react';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
// import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';
import {createAsyncStoragePersister} from "@tanstack/query-async-storage-persister"
import { getQueryClient } from '../../lib/getQueryClient';

export const PersistQueryProvider = ({ children }: { children: ReactNode }) => {
  const client = getQueryClient();
  const persister = useMemo(
    () => createAsyncStoragePersister({ storage: typeof window !== 'undefined' ? window.localStorage : undefined }),
    []
  );

  return (
    <PersistQueryClientProvider
      client={client}
      persistOptions={{
        persister,
        maxAge: 1000 * 60 * 30, // 30 min; tweak for your app
      }}
    >
      {children}
    </PersistQueryClientProvider>
  );
}
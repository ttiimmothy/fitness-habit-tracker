import React, { ReactNode, useEffect, useMemo, useState } from 'react';
import { PersistQueryClientProvider, persistQueryClientRestore } from '@tanstack/react-query-persist-client';
// import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';
import {createAsyncStoragePersister} from "@tanstack/query-async-storage-persister"
import { getQueryClient } from '../../lib/getQueryClient';
import {useAuthStore} from "../../store/authStore";

export const PersistQueryProvider = ({ children }: { children: ReactNode }) => {
  const client = getQueryClient();
  const {user} = useAuthStore()
  const persister = useMemo(
    () => createAsyncStoragePersister({ storage: typeof window !== 'undefined' ? window.localStorage : undefined }),
    []
  );

  // Only create persister in the browser
  // const persister = useMemo(() => {
  //   if (typeof window === 'undefined') return undefined;
  //   return createAsyncStoragePersister({ storage: window.localStorage });
  // }, []);

  // Render a stable placeholder on both SSR and the client's first render
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      if (persister) {
        await persistQueryClientRestore({ queryClient: client, persister });
      }
      if (!cancelled) setReady(true);
    })();
    return () => {
      cancelled = true;
    };
  }, [client, persister]);

  // Same placeholder for SSR and pre-restore client render -> no mismatch
  if (!ready) {
    return <div data-hydration="pending" style={{ minHeight: 1 }} />;
  }

  return (
    <PersistQueryClientProvider
      client={client}
      persistOptions={{
        persister,
        maxAge: 1000 * 60 * 30, // 30 min; tweak for your app
        buster: user?.id ?? 'anon'
      }}
    >
      {children}
    </PersistQueryClientProvider>
  );
}
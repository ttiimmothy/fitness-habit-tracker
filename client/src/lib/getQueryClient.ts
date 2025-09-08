import { QueryClient } from '@tanstack/react-query';

declare global {
  interface Window { __RQ_CLIENT__?: QueryClient }
}

export function getQueryClient() {
  if (typeof window !== 'undefined') {
    window.__RQ_CLIENT__ ??= new QueryClient({
      defaultOptions: {
        queries: { 
          staleTime: 1000 * 60 * 5, // 5 minutes
          retry: 1, 
          refetchOnWindowFocus: false 
        },
        mutations: { retry: 1 },
      },
    });
    return window.__RQ_CLIENT__;
  }
  // Server fallback (islands hydrate on client anyway)
  return new QueryClient();
}
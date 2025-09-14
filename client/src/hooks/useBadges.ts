import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { BadgesResponse } from '../schemas/badgeSchemas';

// Query keys for badges
export const badgeKeys = {
  all: ['badges'] as const,
  user: () => [...badgeKeys.all, 'user'] as const,
};

// Fetch user's badges
export const useBadges = () => {
  return useQuery({
    queryKey: badgeKeys.user(),
    queryFn: async (): Promise<BadgesResponse> => {
      const response = await api('/badges');
      return response.data;
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
    retry: 2,
  });
};

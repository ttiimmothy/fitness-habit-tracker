import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

// Types
export interface Habit {
  id: string;
  name: string;
  description?: string;
  target: number;
  unit: string;
  frequency: 'daily' | 'weekly' | 'monthly';
  createdAt: string;
  updatedAt: string;
}

export interface CreateHabitData {
  name: string;
  description?: string;
  target: number;
  unit: string;
  frequency: 'daily' | 'weekly' | 'monthly';
}

export interface UpdateHabitData extends Partial<CreateHabitData> {
  id: string;
}

// Query keys
export const habitKeys = {
  all: ['habits'] as const,
  lists: () => [...habitKeys.all, 'list'] as const,
  list: (filters: string) => [...habitKeys.lists(), { filters }] as const,
  details: () => [...habitKeys.all, 'detail'] as const,
  detail: (id: string) => [...habitKeys.details(), id] as const,
};

// Custom hooks
export function useHabits() {
  return useQuery({
    queryKey: habitKeys.lists(),
    queryFn: async (): Promise<Habit[]> => {
      const response = await api.get('/habits');
      return response.data;
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useHabit(id: string) {
  return useQuery({
    queryKey: habitKeys.detail(id),
    queryFn: async (): Promise<Habit> => {
      const response = await api.get(`/habits/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
}

export function useCreateHabit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateHabitData): Promise<Habit> => {
      const response = await api.post('/habits', data);
      return response.data;
    },
    onSuccess: () => {
      // Invalidate and refetch habits list
      queryClient.invalidateQueries({ queryKey: habitKeys.lists() });
    },
  });
}

export function useUpdateHabit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, ...data }: UpdateHabitData): Promise<Habit> => {
      const response = await api.put(`/habits/${id}`, data);
      return response.data;
    },
    onSuccess: (updatedHabit) => {
      // Update the specific habit in cache
      queryClient.setQueryData(habitKeys.detail(updatedHabit.id), updatedHabit);
      // Invalidate the habits list
      queryClient.invalidateQueries({ queryKey: habitKeys.lists() });
    },
  });
}

export function useDeleteHabit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      await api.delete(`/habits/${id}`);
    },
    onSuccess: (_, deletedId) => {
      // Remove the habit from cache
      queryClient.removeQueries({ queryKey: habitKeys.detail(deletedId) });
      // Invalidate the habits list
      queryClient.invalidateQueries({ queryKey: habitKeys.lists() });
    },
  });
}

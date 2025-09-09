import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import { CreateHabitFormData } from '../schemas/habitSchemas';

export type Habit = {
  id: string;
  title: string;
  description?: string;
  frequency: 'daily' | 'weekly' | 'monthly';
  target: number;
  category: string;
  color?: string;
  created_at: string;
  updated_at: string;
};

export type HabitDailyProgress = {
  date: string;
  completed: boolean;
  target: number;
  actual: number;
};

// Fetch all habits
export const useHabits = () => {
  return useQuery({
    queryKey: ['habits'],
    queryFn: async (): Promise<Habit[]> => {
      const response = await api('/habits');
      return response.data;
    },
  });
};

// Fetch single habit
export const useHabit = (id: string) => {
  return useQuery({
    queryKey: ['habits', id],
    queryFn: async (): Promise<Habit> => {
      const response = await api(`/habits/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
};

// Create new habit
export const useCreateHabit = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data: CreateHabitFormData): Promise<Habit> => {
      const response = await api.post('/habits', data);
      return response.data;
    },
    onSuccess: () => {
      // Invalidate and refetch habits
      queryClient.invalidateQueries({ queryKey: ['habits'] });
    },
  });
};

// Update habit
export const useUpdateHabit = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<CreateHabitFormData> }): Promise<Habit> => {
      const response = await api.put(`/habits/${id}`, data);
      return response.data;
    },
    onSuccess: (_, { id }) => {
      // Invalidate and refetch habits
      queryClient.invalidateQueries({ queryKey: ['habits'] });
      queryClient.invalidateQueries({ queryKey: ['habits', id] });
    },
  });
};

// Delete habit
export const useDeleteHabit = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      await api.delete(`/habits/${id}`);
    },
    onSuccess: () => {
      // Invalidate and refetch habits
      queryClient.invalidateQueries({ queryKey: ['habits'] });
    },
  });
};

// Fetch daily progress for a specific habit
export const useHabitDailyProgress = (habitId: string, days: number = 7) => {
  return useQuery({
    queryKey: ['habits', habitId, 'daily-progress', days],
    queryFn: async (): Promise<HabitDailyProgress[]> => {
      const response = await api(`/habits/${habitId}/daily-progress?days=${days}`);
      return response.data;
    },
    enabled: !!habitId,
  });
};

// Fetch daily progress for multiple habits
export const useMultipleHabitsDailyProgress = (habitIds: string[], days: number = 7) => {
  return useQuery({
    queryKey: ['habits', 'multiple-daily-progress', habitIds, days],
    queryFn: async (): Promise<Record<string, HabitDailyProgress[]>> => {
      const promises = habitIds.map(habitId => 
        api.get(`/habits/${habitId}/daily-progress?days=${days}`)
          .then(response => ({ habitId, data: response.data }))
      );
      
      const results = await Promise.all(promises);
      const dataMap: Record<string, HabitDailyProgress[]> = {};
      
      results.forEach(({ habitId, data }) => {
        dataMap[habitId] = data;
      });
      
      return dataMap;
    },
    enabled: habitIds.length > 0,
  });
};

// Log habit completion
export const useLogHabit = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      await api.post(`/habits/${id}/log`, {});
    },
    onSuccess: (_, id) => {
      // Invalidate habits and related queries
      queryClient.invalidateQueries({ queryKey: ['habits'] });
      queryClient.invalidateQueries({ queryKey: ['habits', id] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      queryClient.invalidateQueries({ queryKey: ['habits', id, 'daily-progress'] });
      queryClient.invalidateQueries({ queryKey: ['habits', 'multiple-daily-progress'] });
    },
  });
};
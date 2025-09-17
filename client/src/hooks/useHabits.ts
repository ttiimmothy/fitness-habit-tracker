import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import { CreateHabitFormData, UpdateHabitFormData } from '../schemas/habitSchemas';

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

export type HabitProgress = {
  date: string;
  completed: boolean;
  target: number;
  actual: number;
  effective_target: number;
};

export type TodayHabitLog = {
  habit_id: string;
  title: string;
  category: string;
  frequency: string;
  target: number;
  logged_today: boolean;
  current_progress: number; // How many times logged today
  log_id: string | null;
  log_created_at: string | null;
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
    mutationFn: async ({ id, data }: { id: string; data: Partial<UpdateHabitFormData> }): Promise<Habit> => {
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
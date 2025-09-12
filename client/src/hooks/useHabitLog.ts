import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {HabitDailyProgress, TodayHabitLog} from "./useHabits";
import {api} from "../lib/api";

// Log habit completion
export const useLogHabit = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, quantity = 1 }: { id: string; quantity?: number }): Promise<void> => {
      await api.post(`/habits/logs/${id}/log`, { quantity });
    },
    onSuccess: (_, { id }) => {
      // Invalidate habits and related queries
      queryClient.invalidateQueries({ queryKey: ['habits'] });
      queryClient.invalidateQueries({ queryKey: ['habits', id] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      queryClient.invalidateQueries({ queryKey: ['habits', id, 'daily-progress'] });
      queryClient.invalidateQueries({ queryKey: ['habits', 'multiple-daily-progress'] });
      queryClient.invalidateQueries({ queryKey: ['habits', id, 'stats'] });
      queryClient.invalidateQueries({ queryKey: ['habits', 'today-logs-stats'] });
    },
  });
};
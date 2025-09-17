import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {HabitDailyProgress, HabitProgress, TodayHabitLog} from "./useHabits";
import {api} from "../lib/api";

export type HabitStats = {
  habit_id: string;
  current_streak: number;
  longest_streak: number;
  completion_rate: number;
};

interface HabitLog {
  habit_id: string;
  habit_title: string;
  quantity: number;
  target: number;
  logged_at: string;
}

interface DayLogs {
  date: string;
  habits: HabitLog[];
  totalLogs: number;
}

interface CalendarLogsResponse {
  logs: DayLogs[];
  total_days: number;
  total_logs: number;
}

// Fetch daily progress for a specific habit
export const useHabitDailyProgress = (habitId: string, days: number = 7) => {
  return useQuery({
    queryKey: ['habits', habitId, 'daily-progress', days],
    queryFn: async (): Promise<HabitDailyProgress[]> => {
      const response = await api(`/stats/${habitId}/daily-progress?days=${days}`);
      return response.data;
    },
    enabled: !!habitId,
  });
};

// Fetch daily progress for a specific habit
export const useHabitProgress = (habitId: string, days: number = 7) => {
  return useQuery({
    queryKey: ['habits', habitId, 'progress', days],
    queryFn: async (): Promise<HabitProgress[]> => {
      const response = await api(`/stats/${habitId}/progress?days=${days}`);
      return response.data;
    },
    enabled: !!habitId,
  });
};

// Fetch habit stats (streaks, etc.)
export const useHabitStats = (habitId: string) => {
  return useQuery({
    queryKey: ['habits', habitId, 'stats'],
    queryFn: async (): Promise<HabitStats> => {
      const response = await api(`/stats/${habitId}/stats/streak`);
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
        api(`/stats/${habitId}/daily-progress?days=${days}`)
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

// Fetch stats for multiple habits
export const useMultipleHabitsStats = (habitIds: string[]) => {
  return useQuery({
    queryKey: ['habits', 'multiple-stats', habitIds],
    queryFn: async (): Promise<Record<string, HabitStats>> => {
      const promises = habitIds.map(habitId => 
        api(`/stats/${habitId}/stats/streak`)
          .then(response => ({ habitId, data: response.data }))
      );
      
      const results = await Promise.all(promises);
      const dataMap: Record<string, HabitStats> = {};
      
      results.forEach(({ habitId, data }) => {
        dataMap[habitId] = data;
      });
      
      return dataMap;
    },
    enabled: habitIds.length > 0,
  });
};

// Fetch today's habit logs stats
export const useTodayHabitLogsStats = () => {
  return useQuery({
    queryKey: ['habits', 'today-logs-stats'],
    queryFn: async (): Promise<TodayHabitLog[]> => {
      const response = await api('/stats/logs/today');
      return response.data;
    },
  });
};

export function useCalendarLogs(year?: number, month?: number) {
  return useQuery({
    queryKey: ['calendar-logs', year, month],
    queryFn: async (): Promise<DayLogs[]> => {
      const params = new URLSearchParams();
      if (year) params.append('year', year.toString());
      if (month) params.append('month', month.toString());
      
      const response = await api.get(`/stats/overview/calendar`);
      return response.data
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  });
}
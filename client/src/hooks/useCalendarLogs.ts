import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';

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

export function useCalendarLogs(year?: number, month?: number) {
  return useQuery({
    queryKey: ['calendar-logs', year, month],
    queryFn: async (): Promise<DayLogs[]> => {
      const params = new URLSearchParams();
      if (year) params.append('year', year.toString());
      if (month) params.append('month', month.toString());
      
      const response = await api.get(`/stats/overview/calendar`);
      return response.data.logs as DayLogs[];
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  });
}

// Hook for getting logs for a specific date range
export function useDateRangeLogs(startDate: string, endDate: string) {
  return useQuery({
    queryKey: ['calendar-logs-range', startDate, endDate],
    queryFn: async (): Promise<CalendarLogsResponse> => {
      const response = await api.get(`/calendar-logs?start_date=${startDate}&end_date=${endDate}`);
      return response.data;
    },
    enabled: !!startDate && !!endDate,
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
  });
}

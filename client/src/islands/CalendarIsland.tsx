import React from 'react';
import {Calendar} from './react/Calendar';
import { useCalendarLogs } from '../hooks/useStats';
import {QueryProvider} from "../providers/QueryProvider"

interface CalendarIslandProps {
  className?: string;
}

export default function CalendarIsland({ className = '' }: CalendarIslandProps) {
  return (
    <QueryProvider>
      <Calendar/>
    </QueryProvider>
  );
}

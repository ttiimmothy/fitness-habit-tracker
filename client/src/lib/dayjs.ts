import dayjs from 'dayjs';
import weekOfYear from 'dayjs/plugin/weekOfYear';
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';
import customParseFormat from 'dayjs/plugin/customParseFormat';

// Extend dayjs with plugins
dayjs.extend(weekOfYear);
dayjs.extend(isSameOrAfter);
dayjs.extend(isSameOrBefore);
dayjs.extend(customParseFormat);

// Export dayjs as default
export default dayjs;

// Common date utilities
export const dateUtils = {
  // Format date for display
  formatDate: (date: string | Date, format: string = 'YYYY-MM-DD') => {
    return dayjs(date).format(format);
  },

  // Format date for display with locale
  formatDateLocale: (date: string | Date, options: Intl.DateTimeFormatOptions = {}) => {
    return dayjs(date).toDate().toLocaleDateString('en-US', options);
  },

  // Get start of month
  startOfMonth: (date: string | Date) => {
    return dayjs(date).startOf('month');
  },

  // Get end of month
  endOfMonth: (date: string | Date) => {
    return dayjs(date).endOf('month');
  },

  // Get start of week
  startOfWeek: (date: string | Date) => {
    return dayjs(date).startOf('week');
  },

  // Get end of week
  endOfWeek: (date: string | Date) => {
    return dayjs(date).endOf('week');
  },

  // Add days
  addDays: (date: string | Date, days: number) => {
    return dayjs(date).add(days, 'day');
  },

  // Add months
  addMonths: (date: string | Date, months: number) => {
    return dayjs(date).add(months, 'month');
  },

  // Subtract days
  subtractDays: (date: string | Date, days: number) => {
    return dayjs(date).subtract(days, 'day');
  },

  // Subtract months
  subtractMonths: (date: string | Date, months: number) => {
    return dayjs(date).subtract(months, 'month');
  },

  // Check if date is today
  isToday: (date: string | Date) => {
    return dayjs(date).isSame(dayjs(), 'day');
  },

  // Check if date is same month
  isSameMonth: (date1: string | Date, date2: string | Date) => {
    return dayjs(date1).isSame(dayjs(date2), 'month');
  },

  // Check if date is same year
  isSameYear: (date1: string | Date, date2: string | Date) => {
    return dayjs(date1).isSame(dayjs(date2), 'year');
  },

  // Get days in month
  daysInMonth: (date: string | Date) => {
    return dayjs(date).daysInMonth();
  },

  // Get day of week (0 = Sunday, 1 = Monday, etc.)
  dayOfWeek: (date: string | Date) => {
    return dayjs(date).day();
  },

  // Generate array of dates between two dates
  generateDateRange: (startDate: string | Date, endDate: string | Date) => {
    const dates = [];
    let current = dayjs(startDate);
    const end = dayjs(endDate);

    while (current.isSameOrBefore(end)) {
      dates.push(current.toDate());
      current = current.add(1, 'day');
    }

    return dates;
  },

  // Generate array of months between two dates
  generateMonthRange: (startDate: string | Date, endDate: string | Date) => {
    const months = [];
    let current = dayjs(startDate).startOf('month');
    const end = dayjs(endDate).startOf('month');

    while (current.isSameOrBefore(end)) {
      months.push(current.toDate());
      current = current.add(1, 'month');
    }

    return months;
  },

  // Get current date
  now: () => {
    return dayjs().toDate();
  },

  // Get current date as string
  nowString: (format: string = 'YYYY-MM-DD') => {
    return dayjs().format(format);
  },

  // Parse date string
  parse: (dateString: string, format?: string) => {
    return format ? dayjs(dateString, format) : dayjs(dateString);
  },

  // Get difference in days
  diffInDays: (date1: string | Date, date2: string | Date) => {
    return dayjs(date1).diff(dayjs(date2), 'day');
  },

  // Get difference in months
  diffInMonths: (date1: string | Date, date2: string | Date) => {
    return dayjs(date1).diff(dayjs(date2), 'month');
  },

  // Check if date is before another date
  isBefore: (date1: string | Date, date2: string | Date) => {
    return dayjs(date1).isBefore(dayjs(date2));
  },

  // Check if date is after another date
  isAfter: (date1: string | Date, date2: string | Date) => {
    return dayjs(date1).isAfter(dayjs(date2));
  },

  // Check if date is same as another date
  isSame: (date1: string | Date, date2: string | Date, unit: dayjs.OpUnitType = 'day') => {
    return dayjs(date1).isSame(dayjs(date2), unit);
  },

  // Get month names
  getMonthName: (date: string | Date, format: 'short' | 'long' = 'short') => {
    return dayjs(date).format(format === 'short' ? 'MMM' : 'MMMM');
  },

  // Get weekday names
  getWeekdayName: (date: string | Date, format: 'short' | 'long' = 'short') => {
    return dayjs(date).format(format === 'short' ? 'ddd' : 'dddd');
  }
};

import { useState, useEffect, useRef, useMemo } from 'react';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon, ChevronDown } from 'lucide-react';
import {useCalendarLogs} from "../../hooks/useStats";

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

// interface CalendarProps {
//   habitLogs: DayLogs[];
//   // onDateClick?: (date: string) => void;
// }


interface CalendarIslandProps {
  className?: string;
}

export const Calendar = ({ className = '' }: CalendarIslandProps) => {
  const { data: habitLogs, isLoading, error } = useCalendarLogs();

  const [hoveredDate, setHoveredDate] = useState<string | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [currentViewMonth, setCurrentViewMonth] = useState(new Date());
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const initializedRef = useRef(false);
  

  // Calculate the date range from earliest data to current month
  const getDateRange = () => {
    if (!habitLogs || habitLogs.length === 0) {
      const currentDate = new Date();
      return {
        startDate: new Date(currentDate.getFullYear(), currentDate.getMonth(), 1),
        endDate: currentDate
      };
    }

    const dates = habitLogs.map(log => new Date(log.date));
    const earliestDate = new Date(Math.min(...dates.map(d => d.getTime())));
    // const latestDate = new Date(Math.max(...dates.map(d => d.getTime())));
    const currentDate = new Date();

    return {
      startDate: new Date(earliestDate.getFullYear(), earliestDate.getMonth(), 1),
      endDate: new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0)
    };
  };

  const { startDate, endDate } = getDateRange();

  // Generate all months in the range (memoized)
  const months = useMemo(() => {
    const monthsArray = [];
    const currentDate = new Date(startDate);
    
    while (currentDate <= endDate) {
      monthsArray.push(new Date(currentDate));
      currentDate.setMonth(currentDate.getMonth() + 1);
    }
    
    return monthsArray;
  }, [startDate, endDate]);

  // Generate calendar days for a specific month
  const generateCalendarDays = (monthDate: Date) => {
    const firstDayOfMonth = new Date(monthDate.getFullYear(), monthDate.getMonth(), 1);
    const lastDayOfMonth = new Date(monthDate.getFullYear(), monthDate.getMonth() + 1, 0);
    
    // Get first day of calendar grid (might be from previous month)
    const firstDayOfCalendar = new Date(firstDayOfMonth);
    firstDayOfCalendar.setDate(firstDayOfCalendar.getDate() - firstDayOfMonth.getDay());
    
    // Calculate the number of weeks needed for this month
    const lastDayOfCalendar = new Date(lastDayOfMonth);
    lastDayOfCalendar.setDate(lastDayOfCalendar.getDate() + (6 - lastDayOfMonth.getDay()));
    
    const totalDays = Math.ceil((lastDayOfCalendar.getTime() - firstDayOfCalendar.getTime()) / (1000 * 60 * 60 * 24)) + 1;
    const weeksNeeded = Math.ceil(totalDays / 7);
    
    const calendarDays = [];
    const currentDateObj = new Date(firstDayOfCalendar);
    
    for (let i = 0; i < weeksNeeded * 7; i++) {
      calendarDays.push(new Date(currentDateObj));
      currentDateObj.setDate(currentDateObj.getDate() + 1);
    }
    
    return calendarDays;
  };

  // Get logs for a specific date
  const getLogsForDate = (date: Date): DayLogs | null => {
    const dateStr = date.toISOString().split('T')[0];
    return habitLogs?.find(log => log.date === dateStr) || null;
  };

  // Check if date has logs
  const hasLogs = (date: Date): boolean => {
    return getLogsForDate(date) !== null;
  };

  // Get completion rate for a date
  const getCompletionRate = (date: Date): number => {
    const dayLogs = getLogsForDate(date);
    if (!dayLogs || dayLogs.habits.length === 0) return 0;
    
    const totalTarget = dayLogs.habits.reduce((sum, habit) => sum + habit.target, 0);
    const totalLogged = dayLogs.habits.reduce((sum, habit) => sum + habit.quantity, 0);
    
    return totalTarget > 0 ? Math.min((totalLogged / totalTarget) * 100, 100) : 0;
  };


  // Scroll to specific month
  const scrollToMonth = (monthIndex: number) => {
    if (scrollContainerRef.current) {
      const gridContainer = scrollContainerRef.current.querySelector('.grid') as HTMLElement;
      if (gridContainer) {
        const monthElement = gridContainer.children[monthIndex] as HTMLElement;
        if (monthElement) {
          monthElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    }
  };

  // Navigate to previous/next month
  const goToPreviousMonth = () => {
    const currentIndex = months.findIndex(month => 
      month.getMonth() === currentViewMonth.getMonth() && 
      month.getFullYear() === currentViewMonth.getFullYear()
    );
    if (currentIndex > 0) {
      const prevMonth = months[currentIndex - 1];
      setCurrentViewMonth(prevMonth);
      scrollToMonth(currentIndex - 1);
    }
  };

  const goToNextMonth = () => {
    const currentIndex = months.findIndex(month => 
      month.getMonth() === currentViewMonth.getMonth() && 
      month.getFullYear() === currentViewMonth.getFullYear()
    );
    if (currentIndex < months.length - 1) {
      const nextMonth = months[currentIndex + 1];
      setCurrentViewMonth(nextMonth);
      scrollToMonth(currentIndex + 1);
    }
  };

  // Handle month selection from dropdown
  const handleMonthSelect = (selectedMonth: Date) => {
    setCurrentViewMonth(selectedMonth);
    const monthIndex = months.findIndex(month => 
      month.getMonth() === selectedMonth.getMonth() && 
      month.getFullYear() === selectedMonth.getFullYear()
    );
    if (monthIndex !== -1) {
      scrollToMonth(monthIndex);
    }
    setIsDropdownOpen(false);
  };

  // Scroll to current month on mount
  useEffect(() => {
    if (initializedRef.current || months.length === 0) return;
    
    const currentDate = new Date();
    const currentMonthIndex = months.findIndex(month => 
      month.getMonth() === currentDate.getMonth() && 
      month.getFullYear() === currentDate.getFullYear()
    );
    
    if (currentMonthIndex !== -1) {
      setCurrentViewMonth(months[currentMonthIndex]);
      setTimeout(() => scrollToMonth(currentMonthIndex), 100);
      initializedRef.current = true;
    }
  }, [months]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isDropdownOpen) {
        const target = event.target as Element;
        if (!target.closest('.relative')) {
          setIsDropdownOpen(false);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isDropdownOpen]);

  // Handle mouse events for tooltip
  const handleMouseEnter = (date: Date, event: React.MouseEvent) => {
    if (hasLogs(date)) {
      setHoveredDate(date.toISOString().split('T')[0]);
      setTooltipPosition({ x: event.clientX, y: event.clientY });
    }
  };

  const handleMouseLeave = () => {
    setHoveredDate(null);
  };

  const handleMouseMove = (event: React.MouseEvent) => {
    if (hoveredDate) {
      setTooltipPosition({ x: event.clientX, y: event.clientY });
    }
  };

  // Get month name
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  // Group months by year for dropdown
  const monthsByYear = useMemo(() => {
    const grouped: { [year: number]: Date[] } = {};
    months.forEach(month => {
      const year = month.getFullYear();
      if (!grouped[year]) {
        grouped[year] = [];
      }
      grouped[year].push(month);
    });
    return grouped;
  }, [months]);


  if (isLoading) {
    return (
      <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded mb-4"></div>
          <div className="grid grid-cols-7 gap-1">
            {Array.from({ length: 42 }).map((_, i) => (
              <div key={i} className="h-12 bg-gray-200 dark:bg-gray-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 ${className}`}>
        <div className="text-center text-red-500">
          <p>Failed to load calendar data</p>
          <p className="text-sm text-gray-500 mt-1">Please try refreshing the page</p>
        </div>
      </div>
    );
  }

  // Render a single month
  const renderMonth = (monthDate: Date, monthIndex: number) => {
    const calendarDays = generateCalendarDays(monthDate);
    const isCurrentMonth = monthDate.getMonth() === new Date().getMonth() && monthDate.getFullYear() === new Date().getFullYear();

    return (
      <div key={monthIndex} className="w-full">
        {/* Month Header */}
        <div className="flex items-center justify-between mb-3">
          <h3 className={`text-sm font-semibold ${isCurrentMonth ? 'text-blue-600 dark:text-blue-400' : 'text-gray-900 dark:text-white'}`}>
            {monthNames[monthDate.getMonth()]} {monthDate.getFullYear()}
          </h3>
          {isCurrentMonth && (
            <div className="flex items-center text-xs text-blue-600 dark:text-blue-400">
              <CalendarIcon className="h-3 w-3 mr-1" />
              Current
            </div>
          )}
        </div>

        {/* Calendar Grid */}
        <div 
          className="grid grid-cols-7 gap-0.5"
          style={{
            gridTemplateRows: `repeat(${Math.ceil(calendarDays.length / 7)}, minmax(2rem, auto))`
          }}
        >
          {/* Day headers */}
          {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, dayIndex) => (
            <div key={`${monthDate.getFullYear()}-${monthDate.getMonth()}-header-${dayIndex}`} className="p-1 text-center text-xs font-medium text-gray-500 dark:text-gray-400">
              {day}
            </div>
          ))}

          {/* Calendar days */}
          {calendarDays.map((date, index) => {
            const isCurrentMonth = date.getMonth() === monthDate.getMonth();
            const isToday = date.toDateString() === new Date().toDateString();
            const dayLogs = getLogsForDate(date);
            const completionRate = getCompletionRate(date);
            const hasLogsToday = hasLogs(date);

            return (
              <div
                key={`${monthDate.getFullYear()}-${monthDate.getMonth()}-day-${date.getDate()}-${index}`}
                className={`
                  relative p-1 h-8 flex items-center justify-center text-xs cursor-pointer
                  transition-all duration-200 rounded
                  ${isCurrentMonth 
                    ? 'text-gray-900 dark:text-white' 
                    : 'text-gray-400 dark:text-gray-600'
                  }
                  ${isToday 
                    ? 'bg-blue-100 dark:bg-blue-900/30 font-semibold' 
                    : hasLogsToday 
                      ? 'hover:bg-green-50 dark:hover:bg-green-900/20' 
                      : 'hover:bg-gray-100 dark:hover:bg-gray-600'
                  }
                `}
                onMouseEnter={(e) => handleMouseEnter(date, e)}
                onMouseLeave={handleMouseLeave}
                onMouseMove={handleMouseMove}
                // onClick={() => onDateClick?.(date.toISOString().split('T')[0])}
              >
                {date.getDate()}
                
                {/* Visual indicator for days with logs */}
                {hasLogsToday && (
                  <div className="absolute bottom-0.5 left-1/2 transform -translate-x-1/2">
                    <div 
                      className={`
                        w-1.5 h-1.5 rounded-full
                        ${completionRate >= 100 
                          ? 'bg-green-500' 
                          : completionRate >= 50 
                            ? 'bg-yellow-500' 
                            : 'bg-orange-500'
                        }
                      `}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="rounded-lg py-4">
      {/* Timeline Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center">
            <CalendarIcon className="h-6 w-6 mr-2" />
            Habit Calendar
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {months.length} months of data - {habitLogs?.length} days with logs
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={goToPreviousMonth}
            disabled={months.findIndex(month => 
              month.getMonth() === currentViewMonth.getMonth() && 
              month.getFullYear() === currentViewMonth.getFullYear()
            ) === 0}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="h-5 w-5" />
          </button>
          
          {/* Month/Year Dropdown */}
          <div className="relative">
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <span>{monthNames[currentViewMonth.getMonth()]} {currentViewMonth.getFullYear()}</span>
              <ChevronDown className="h-4 w-4" />
            </button>
            
            {/* Dropdown Menu */}
            {isDropdownOpen && (
              <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-64 max-h-80 overflow-y-auto bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
                <div className="p-2">
                  {Object.keys(monthsByYear)
                    // .sort((a, b) => parseInt(b) - parseInt(a)) // Sort years descending
                    .map(year => (
                      <div key={year} className="mb-2">
                        <div className="px-3 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                          {year}
                        </div>
                        <div className="space-y-1">
                          {monthsByYear[parseInt(year)]
                            .sort((a, b) => a.getMonth() - b.getMonth()) // Sort months ascending
                            .map(month => {
                              const isSelected = month.getMonth() === currentViewMonth.getMonth() && month.getFullYear() === currentViewMonth.getFullYear();
                              const isCurrentMonth = month.getMonth() === new Date().getMonth() && month.getFullYear() === new Date().getFullYear();
                              
                              return (
                                <button
                                  key={`${month.getFullYear()}-${month.getMonth()}`}
                                  onClick={() => handleMonthSelect(month)}
                                  className={`w-full text-left px-3 py-2 text-sm rounded-md transition-colors flex items-center justify-between ${
                                    isSelected
                                      ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                                      : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                                  }`}
                                >
                                  <span>{monthNames[month.getMonth()]}</span>
                                  {isCurrentMonth && (
                                    <div className="flex items-center text-xs text-blue-600 dark:text-blue-400">
                                      <CalendarIcon className="h-3 w-3 mr-1" />
                                      Current
                                    </div>
                                  )}
                                </button>
                              );
                            })}
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>
          
          <button
            onClick={goToNextMonth}
            disabled={months.findIndex(month => 
              month.getMonth() === currentViewMonth.getMonth() && 
              month.getFullYear() === currentViewMonth.getFullYear()
            ) === months.length - 1}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronRight className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Grid Timeline - 4 months per row */}
      <div 
        ref={scrollContainerRef}
        className="max-h-[48rem] overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-gray-100 dark:scrollbar-track-gray-800 p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {months.map((month, index) => (
            <div key={`month-${month.getFullYear()}-${month.getMonth()}`} className="bg-white dark:bg-gray-700 rounded-lg p-4">
              {renderMonth(month, index)}
            </div>
          ))}
        </div>
      </div>

      {/* Tooltip */}
      {hoveredDate && (
        <div
          className="fixed z-50 bg-gray-900 dark:bg-gray-700 text-white text-sm rounded-lg shadow-lg p-3 max-w-xs"
          style={{
            left: tooltipPosition.x + 10,
            top: tooltipPosition.y - 10,
            pointerEvents: 'none'
          }}
        >
          {(() => {
            const dayLogs = getLogsForDate(new Date(hoveredDate));
            if (!dayLogs) return null;

            return (
              <div>
                <div className="font-semibold mb-2">
                  {new Date(hoveredDate).toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}
                </div>
                <div className="space-y-1">
                  {dayLogs.habits.map((habit, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="truncate mr-2">{habit.habit_title}</span>
                      <span className="text-green-400 font-medium">
                        {habit.quantity}/{habit.target}
                      </span>
                    </div>
                  ))}
                </div>
                <div className="mt-2 pt-2 border-t border-gray-600">
                  <div className="text-xs text-gray-300">
                    Total: {dayLogs.totalLogs} logs
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
}

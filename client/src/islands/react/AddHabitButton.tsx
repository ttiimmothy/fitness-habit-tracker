import React, { useState, useEffect } from 'react';
import { Plus, X } from 'lucide-react';
import AddHabitForm from './AddHabitForm';

const AddHabitButton = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const openSidebar = () => {
    setIsSidebarOpen(true);
  };

  const closeSidebar = () => {
    setIsSidebarOpen(false);
  };

  // Handle ESC key to close sidebar
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isSidebarOpen) {
        closeSidebar();
      }
    };

    if (isSidebarOpen) {
      document.addEventListener('keydown', handleEscKey);
      // Prevent body scroll when sidebar is open
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
      document.body.style.overflow = 'unset';
    };
  }, [isSidebarOpen]);

  // Close sidebar when clicking outside
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      closeSidebar();
    }
  };

  return (
    <>
      {/* Add Habit Button */}
      <button
        onClick={openSidebar}
        className="w-full p-6 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors group"
      >
        <div className="flex flex-col items-center justify-center space-y-2">
          <div className="p-3 rounded-full bg-blue-100 dark:bg-blue-900/30 group-hover:bg-blue-200 dark:group-hover:bg-blue-900/50 transition-colors">
            <Plus className="h-6 w-6 text-blue-600 dark:text-blue-400" />
          </div>
          <div className="text-center">
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">Add New Habit</p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Click to create a new habit</p>
          </div>
        </div>
      </button>

      {/* Add Habit Sidebar Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 z-50 overflow-hidden"
        >
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-black bg-opacity-50 transition-opacity" 
            onClick={handleBackdropClick}
          />
          
          {/* Sidebar */}
          <div className="absolute right-0 top-0 h-full w-full max-w-md bg-white dark:bg-gray-800 shadow-xl transform transition-transform">
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-medium text-gray-900 dark:text-white">Add New Habit</h2>
                <button
                  onClick={closeSidebar}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              {/* Content */}
              <div className="flex-1 overflow-y-auto">
                <div className="p-6">
                  <AddHabitForm onSuccess={closeSidebar} />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default AddHabitButton
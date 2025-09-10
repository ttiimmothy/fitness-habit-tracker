import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import UpdateHabitForm from './UpdateHabitForm';

interface UpdateHabitSidebarProps {
  habit: {
    id: string;
    title: string;
    description?: string;
    category: string;
    frequency: string;
    target: number;
    color?: string;
  };
  isOpen: boolean;
  onClose: () => void;
}

const UpdateHabitSidebar = ({ habit, isOpen, onClose }: UpdateHabitSidebarProps) => {
  // Handle ESC key to close sidebar
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscKey);
      // Prevent body scroll when sidebar is open
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  // Close sidebar when clicking outside
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
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
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">Update Habit</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
          
          {/* Content */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-6">
              <UpdateHabitForm 
                habit={habit} 
                onSuccess={onClose} 
                onCancel={onClose} 
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UpdateHabitSidebar;

import React, { useEffect } from 'react';
import { X } from 'lucide-react';
import UpdateUsernameForm from './UpdateUsernameForm';

interface UpdateUsernameSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  currentName: string;
}

export default function UpdateUsernameSidebar({ isOpen, onClose, currentName }: UpdateUsernameSidebarProps) {
  useEffect(() => {
    if (isOpen) {
      // Prevent body scroll when sidebar is open
      document.body.style.overflow = 'hidden';
    } else {
      // Restore body scroll when sidebar is closed
      document.body.style.overflow = 'unset';
    }

    // Cleanup on unmount
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />
      
      {/* Sidebar */}
      <div className="absolute right-0 top-0 h-full w-full max-w-md bg-white dark:bg-gray-800 shadow-xl transform transition-transform">
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Update Username
            </h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
            >
              <X className="h-5 w-5 text-gray-500 dark:text-gray-400" />
            </button>
          </div>
          
          {/* Content */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-6">
            <UpdateUsernameForm 
              currentName={currentName}
              onSuccess={onClose}
            />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

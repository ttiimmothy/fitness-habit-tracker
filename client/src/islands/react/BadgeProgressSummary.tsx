import React from 'react';
import { useBadges } from '../../hooks/useBadges';

export const BadgeProgressSummary = () => {
  const { data: badgesData, isLoading, error } = useBadges();

  if (isLoading) {
    return (
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-6 text-white">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Your Badge Progress</h2>
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gradient-to-r from-red-500 to-red-600 rounded-xl p-6 text-white">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Your Badge Progress</h2>
          <p className="text-red-100">Failed to load badge data</p>
        </div>
      </div>
    );
  }

  if (!badgesData) {
    return (
      <div className="bg-gradient-to-r from-gray-500 to-gray-600 rounded-xl p-6 text-white">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Your Badge Progress</h2>
          <p className="text-gray-100">No badge data available</p>
        </div>
      </div>
    );
  }

  const inProgressBadges = badgesData.categories.reduce((total, category) => {
    return total + category.badges.filter(badge => badge.status === 'in_progress').length;
  }, 0);

  return (
    <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-6 text-white">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Your Badge Progress</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <div className="text-center">
            <div className="text-3xl font-bold">{badgesData.earned_badges}</div>
            <div className="text-blue-100">Badges Earned</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">{inProgressBadges}</div>
            <div className="text-blue-100">In Progress</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">{badgesData.total_badges}</div>
            <div className="text-blue-100">Total Available</div>
          </div>
        </div>
        
        {/* Progress Bar */}
        <div className="mt-6">
          <div className="flex justify-between text-sm text-blue-100 mb-2">
            <span>Overall Progress</span>
            <span>{badgesData.completion_percentage}%</span>
          </div>
          <div className="w-full bg-blue-300 bg-opacity-30 rounded-full h-3">
            <div 
              className="bg-white h-3 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${badgesData.completion_percentage}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

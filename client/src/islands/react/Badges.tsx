import React, { useState } from 'react';
import { useBadges } from '../../hooks/useBadges';
import { Badge, BadgeCategory } from '../../schemas/badgeSchemas';
import { BadgeModal } from './BadgeModal';

const BadgeCard = ({ badge, onClick }: { badge: Badge; onClick: () => void }) => {
  const getStatusBadge = () => {
    switch (badge.status) {
      case 'earned':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
            ✓ Earned
          </span>
        );
      case 'in_progress':
        const progress = badge.progress;
        const percentage = progress ? Math.round((progress.current / progress.target) * 100) : 0;
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300">
            🔥 {progress?.current || 0}/{progress?.target || 0}
          </span>
        );
      case 'locked':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 dark:bg-gray-600 dark:text-gray-400">
            🔒 Locked
          </span>
        );
      default:
        return null;
    }
  };

  const getCardStyles = () => {
    switch (badge.status) {
      case 'earned':
        return 'bg-green-50 dark:bg-green-900/20';
      case 'in_progress':
        return 'bg-orange-50 dark:bg-orange-900/20';
      case 'locked':
        return 'bg-gray-50 dark:bg-gray-700 opacity-60';
      default:
        return 'bg-gray-50 dark:bg-gray-700';
    }
  };

  const getIconClasses = () => {
    const baseClasses = "w-12 h-12 transition-all duration-300";
    
    if (badge.status === 'earned') {
      return `${baseClasses} text-yellow-500`;
    } else if (badge.status === 'in_progress') {
      return `${baseClasses} text-blue-500`;
    } else {
      return `${baseClasses} text-gray-400`;
    }
  };

  return (
    <div 
      className={`flex items-center p-3 rounded-lg cursor-pointer hover:shadow-md transition-all duration-200 ${getCardStyles()}`}
      onClick={onClick}
    >
      <div className="w-12 h-12 mr-3 flex-shrink-0">
        {badge.icon_url ? (
          <img 
            src={badge.icon_url} 
            alt={badge.title} 
            className={getIconClasses()}
          />
        ) : badge.emoji ? (
          <div className={`${getIconClasses()} flex items-center justify-center text-2xl`}>
            {badge.emoji}
          </div>
        ) : (
          <div className={`${getIconClasses()} bg-gray-200 dark:bg-gray-600 rounded-full flex items-center justify-center`}>
            🏆
          </div>
        )}
      </div>
      <div className="flex-1 min-w-0">
        <h3 className="font-medium text-gray-900 dark:text-white">{badge.title}</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 h-10 leading-5 overflow-hidden line-clamp-2">
          {badge.description}
        </p>
        <div className="mt-1">
          {getStatusBadge()}
        </div>
      </div>
    </div>
  );
};

const BadgeCategorySection = ({ category, onBadgeClick }: { category: BadgeCategory; onBadgeClick: (badge: Badge) => void }) => {
  const getCategoryIcon = () => {
    switch (category.id) {
      case 'first_steps':
        return '🌱';
      case 'consistency':
        return '🔥';
      case "special_achievements":
        return "⭐";
      case 'fitness':
        return '💪';
      case "wellness":
        return "🧘";
      case 'social':
        return '👥';
      default:
        return '🏆';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
        <span className="text-2xl mr-2">{getCategoryIcon()}</span>
        {category.name}
      </h2>
      
      <div className="space-y-4">
        {category.badges.map((badge) => (
          <BadgeCard key={badge.id} badge={badge} onClick={() => onBadgeClick(badge)} />
        ))}
      </div>
    </div>
  );
};

export const Badges  = () => {
  const { data: badgesData, isLoading, error } = useBadges();
  const [selectedBadge, setSelectedBadge] = useState<Badge | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleBadgeClick = (badge: Badge) => {
    setSelectedBadge(badge);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedBadge(null);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading badges...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
              Error loading badges
            </h3>
            <div className="mt-2 text-sm text-red-700 dark:text-red-300">
              <p>Failed to load your achievement badges. Please try again later.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!badgesData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 dark:text-gray-400">No badge data available.</p>
      </div>
    );
  }

  const inProgressBadges = badgesData.categories.reduce((total, category) => {
    return total + category.badges.filter(badge => badge.status === 'in_progress').length;
  }, 0);

  return (
    <main className="space-y-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Achievement Badges
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          Earn badges by completing habits and reaching milestones!
        </p>
        
        {/* Progress Summary */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 max-w-md mx-auto">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600 dark:text-gray-400">Progress</span>
            <span className="font-medium text-gray-900 dark:text-white">
              {badgesData.earned_badges}/{badgesData.total_badges} badges
            </span>
          </div>
          <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${badgesData.completion_percentage}%` }}
            ></div>
          </div>
          <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {badgesData.completion_percentage}% complete
          </p>
        </div>
      </div>

      {/* Badge Categories */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {badgesData.categories.map((category) => (
          <BadgeCategorySection key={category.id} category={category} onBadgeClick={handleBadgeClick} />
        ))}
      </div>


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

      {/* Badge Modal */}
      {selectedBadge && (
        <BadgeModal
          badge={selectedBadge}
          isOpen={isModalOpen}
          onClose={handleCloseModal}
        />
      )}

    </main>
  );
};

import React from 'react';
import { Badge, BadgeStatus } from '../../schemas/badgeSchemas';

interface BadgeModalProps {
  badge: Badge;
  isOpen: boolean;
  onClose: () => void;
}

const getBadgeDescription = (badgeId: string): string => {
  const descriptions: Record<string, string> = {
    first_habit: "Create your first habit to unlock this badge! Start your journey by adding any habit that matters to you.",
    first_log: "Log your first habit entry to earn this badge! Track your progress by logging your habit completion.",
    week_warrior: "Log habits for 7 consecutive days to earn this badge! Build consistency by maintaining your streak.",
    streak_master: "Maintain a 30-day logging streak to earn this badge! This shows incredible dedication and consistency.",
    workout_warrior: "Complete 50 fitness-related habit entries to earn this badge! Focus on physical activities and exercise.",
    sharing_champion: "Share your progress 10 times to earn this badge! Help motivate others by sharing your journey.",
    perfect_week: "Complete ALL your habits for 7 consecutive days to earn this badge! This requires perfect consistency across all habits.",
    early_bird: "Log habits before 7 AM for 5 days to earn this badge! Start your day with healthy habits.",
    night_owl: "Log habits after 10 PM for 5 days to earn this badge! End your day with positive habits.",
    habit_creator: "Create 10 different habits to earn this badge! Build a comprehensive habit system.",
    cardio_king: "Complete 30 cardio-related activities to earn this badge! Focus on heart-pumping exercises.",
    flexibility_master: "Complete 20 flexibility activities (stretching, yoga, etc.) to earn this badge! Improve your mobility and flexibility.",
    meditation_master: "Meditate for 100 minutes total to earn this badge! Practice mindfulness and mental wellness.",
    hydration_hero: "Log hydration habits for 14 consecutive days to earn this badge! Stay consistently hydrated.",
    sleep_champion: "Track your sleep for 21 consecutive days to earn this badge! Prioritize rest and recovery.",
    motivator: "Motivate other users 5 times to earn this badge! Help build a supportive community.",
    community_helper: "Help other community members 3 times to earn this badge! Contribute to the community spirit."
  };
  
  return descriptions[badgeId] || "Complete the requirements to earn this badge!";
};

const getProgressText = (badge: Badge): string => {
  if (badge.status === 'earned') {
    return `Completed! You earned this badge on ${new Date(badge.earned_at!).toLocaleDateString()}`;
  } else if (badge.status === 'in_progress' && badge.progress) {
    return `Progress: ${badge.progress.current}/${badge.progress.target} (${Math.round((badge.progress.current / badge.progress.target) * 100)}%)`;
  } else {
    return `Locked - Complete the requirements to unlock this badge`;
  }
};

export const BadgeModal: React.FC<BadgeModalProps> = ({ badge, isOpen, onClose }) => {
  if (!isOpen) return null;

  const description = getBadgeDescription(badge.id);
  const progressText = getProgressText(badge);

  const getIconClasses = () => {
    const baseClasses = "w-24 h-24 mx-auto mb-4 transition-all duration-300";
    
    if (badge.status === 'earned') {
      return `${baseClasses} text-yellow-500`;
    } else if (badge.status === 'in_progress') {
      return `${baseClasses} text-blue-500`;
    } else {
      return `${baseClasses} text-gray-400`;
    }
  };


  const getStatusColor = () => {
    if (badge.status === 'earned') {
      return 'text-yellow-600 dark:text-yellow-400';
    } else if (badge.status === 'in_progress') {
      return 'text-blue-600 dark:text-blue-400';
    } else {
      return 'text-gray-500 dark:text-gray-400';
    }
  };

  const getProgressBarColor = () => {
    if (badge.status === 'earned') {
      return 'bg-yellow-500';
    } else if (badge.status === 'in_progress') {
      return 'bg-blue-500';
    } else {
      return 'bg-gray-400';
    }
  };

  return (
    <div className="modal-backdrop flex items-center justify-center">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto m-4">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            {badge.title}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Badge Icon */}
          <div className="text-center mb-6">
            <div className={`w-24 h-24 mx-auto mb-4 flex items-center justify-center`}>
              {badge.icon_url ? (
                <img 
                  src={badge.icon_url} 
                  alt={badge.title} 
                  className={`w-full h-full object-contain ${badge.status === 'locked' ? 'grayscale opacity-60' : ''}`}
                />
              ) : badge.emoji ? (
                <div className={`${getIconClasses()} flex items-center justify-center text-4xl`}>
                  {badge.emoji}
                </div>
              ) : (
                <div className={`${getIconClasses()} ${
                  badge.status === 'earned' 
                    ? 'bg-gradient-to-br from-yellow-400 to-yellow-600 dark:from-yellow-500 dark:to-yellow-700' 
                    : badge.status === 'in_progress' 
                    ? 'bg-gradient-to-br from-blue-400 to-blue-600 dark:from-blue-500 dark:to-blue-700'
                    : 'bg-gradient-to-br from-gray-400 to-gray-600 dark:from-gray-500 dark:to-gray-700'
                } rounded-full flex items-center justify-center shadow-lg`}>
                  {/* 3D Isometric Trophy Icon */}
                  <svg 
                    className={`w-24 h-24 trophy-3d ${
                      badge.status === 'earned' 
                        ? 'trophy-3d-earned' 
                        : badge.status === 'in_progress' 
                        ? 'trophy-3d-progress' 
                        : 'trophy-3d-locked'
                    }`}
                    fill="currentColor" 
                    viewBox="0 0 48 48"
                    style={{ shapeRendering: 'geometricPrecision' }}
                  >
                    <defs>
                      {/* 3D Isometric Gradients */}
                      <linearGradient id={`trophyTop-${badge.status}`} x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor={badge.status === 'earned' ? '#FFD700' : badge.status === 'in_progress' ? '#60A5FA' : '#D1D5DB'}/>
                        <stop offset="50%" stopColor={badge.status === 'earned' ? '#FFA500' : badge.status === 'in_progress' ? '#3B82F6' : '#9CA3AF'}/>
                        <stop offset="100%" stopColor={badge.status === 'earned' ? '#B8860B' : badge.status === 'in_progress' ? '#1E40AF' : '#6B7280'}/>
                      </linearGradient>
                      <linearGradient id={`trophyLeft-${badge.status}`} x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor={badge.status === 'earned' ? '#B8860B' : badge.status === 'in_progress' ? '#1E40AF' : '#6B7280'}/>
                        <stop offset="100%" stopColor={badge.status === 'earned' ? '#8B6914' : badge.status === 'in_progress' ? '#1E3A8A' : '#4B5563'}/>
                      </linearGradient>
                      <linearGradient id={`trophyRight-${badge.status}`} x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor={badge.status === 'earned' ? '#FFA500' : badge.status === 'in_progress' ? '#3B82F6' : '#9CA3AF'}/>
                        <stop offset="100%" stopColor={badge.status === 'earned' ? '#FF8C00' : badge.status === 'in_progress' ? '#2563EB' : '#6B7280'}/>
                      </linearGradient>
                      <linearGradient id={`trophyBase-${badge.status}`} x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor={badge.status === 'earned' ? '#DAA520' : badge.status === 'in_progress' ? '#2563EB' : '#6B7280'}/>
                        <stop offset="100%" stopColor={badge.status === 'earned' ? '#B8860B' : badge.status === 'in_progress' ? '#1E40AF' : '#374151'}/>
                      </linearGradient>
                    </defs>
                    
                    {/* Trophy Base - 3D Isometric */}
                    <path d="M8 32L16 28L32 28L40 32L40 36L32 40L16 40L8 36Z" 
                          fill={`url(#trophyBase-${badge.status})`}/>
                    
                    {/* Trophy Base - Left Side */}
                    <path d="M8 32L16 28L16 40L8 36Z" 
                          fill={badge.status === 'earned' ? '#8B6914' : badge.status === 'in_progress' ? '#1E3A8A' : '#4B5563'}/>
                    
                    {/* Trophy Base - Right Side */}
                    <path d="M32 28L40 32L40 36L32 40Z" 
                          fill={badge.status === 'earned' ? '#B8860B' : badge.status === 'in_progress' ? '#1E40AF' : '#6B7280'}/>
                    
                    {/* Trophy Cup - Top Face */}
                    <path d="M16 8L24 4L32 8L32 20L24 24L16 20Z" 
                          fill={`url(#trophyTop-${badge.status})`}/>
                    
                    {/* Trophy Cup - Left Face */}
                    <path d="M16 8L16 20L8 16L8 12Z" 
                          fill={`url(#trophyLeft-${badge.status})`}/>
                    
                    {/* Trophy Cup - Right Face */}
                    <path d="M32 8L40 12L40 16L32 20Z" 
                          fill={`url(#trophyRight-${badge.status})`}/>
                    
                    {/* Trophy Handle - 3D Isometric */}
                    <path d="M20 12L24 10L28 12L28 20L24 22L20 20Z" 
                          fill={badge.status === 'earned' ? '#FF8C00' : badge.status === 'in_progress' ? '#60A5FA' : '#D1D5DB'}/>
                    
                    {/* Trophy Handle - Left Side */}
                    <path d="M20 12L20 20L16 18L16 14Z" 
                          fill={badge.status === 'earned' ? '#B8860B' : badge.status === 'in_progress' ? '#1E40AF' : '#6B7280'}/>
                    
                    {/* Trophy Handle - Right Side */}
                    <path d="M28 12L32 14L32 18L28 20Z" 
                          fill={badge.status === 'earned' ? '#FFA500' : badge.status === 'in_progress' ? '#3B82F6' : '#9CA3AF'}/>
                    
                    {/* Trophy Star - 3D Isometric */}
                    <path d="M24 6L26 10L30 10L27 13L28 17L24 15L20 17L21 13L18 10L22 10Z" 
                          fill={badge.status === 'earned' ? '#FFFFFF' : badge.status === 'in_progress' ? '#FFFFFF' : '#F3F4F6'}/>
                    
                    {/* 3D Shadow and Depth Lines */}
                    <path d="M8 32L16 28L32 28L40 32" 
                          fill="none" 
                          stroke={badge.status === 'earned' ? '#8B6914' : badge.status === 'in_progress' ? '#1E3A8A' : '#4B5563'} 
                          strokeWidth="0.5"/>
                    <path d="M16 8L24 4L32 8" 
                          fill="none" 
                          stroke={badge.status === 'earned' ? '#B8860B' : badge.status === 'in_progress' ? '#1E40AF' : '#6B7280'} 
                          strokeWidth="0.5"/>
                    <path d="M32 8L40 12L40 16L32 20" 
                          fill="none" 
                          stroke={badge.status === 'earned' ? '#FFA500' : badge.status === 'in_progress' ? '#3B82F6' : '#9CA3AF'} 
                          strokeWidth="0.5"/>
                  </svg>
                </div>
              )}
            </div>
            <div className={`text-sm font-medium ${getStatusColor()}`}>
              {badge.status === 'earned' ? 'Earned!' : 
               badge.status === 'in_progress' ? 'In Progress' : 'Locked'}
            </div>
          </div>

          {/* Description */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Description
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
              {badge.description}
            </p>
          </div>

          {/* How to Earn */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              How to Earn
            </h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
              {description}
            </p>
          </div>

          {/* Progress */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Progress
            </h3>
            <p className={`text-sm mb-3 ${getStatusColor()}`}>
              {progressText}
            </p>
            
            {badge.status !== 'locked' && badge.progress && (
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${getProgressBarColor()}`}
                  style={{
                    width: `${Math.min((badge.progress.current / badge.progress.target) * 100, 100)}%`
                  }}
                />
              </div>
            )}
          </div>

          {/* Category */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Category
            </h3>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
              {badge.category.replace('_', ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

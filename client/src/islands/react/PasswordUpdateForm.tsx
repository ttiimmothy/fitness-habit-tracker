import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import toast from 'react-hot-toast';
import { api } from '../../lib/api';

// Password update validation schema
const passwordUpdateSchema = z.object({
  currentPassword: z
    .string()
    .min(1, 'Current password is required'),
  newPassword: z
    .string()
    .min(1, 'New password is required')
    .min(2, 'New password must be at least 2 characters')
    .max(100, 'New password must be less than 100 characters'),
  confirmPassword: z
    .string()
    .min(1, 'Please confirm your new password'),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "New passwords don't match",
  path: ["confirmPassword"],
});

type PasswordUpdateFormData = z.infer<typeof passwordUpdateSchema>;

interface PasswordUpdateFormProps {
  onSuccess?: () => void;
}

export default function PasswordUpdateForm({ onSuccess }: PasswordUpdateFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<PasswordUpdateFormData>({
    resolver: zodResolver(passwordUpdateSchema),
  });

  const onSubmit = async (data: PasswordUpdateFormData) => {
    setIsSubmitting(true);

    try {
      await api.post('/auth/change-password', {
        currentPassword: data.currentPassword,
        newPassword: data.newPassword,
      });

      toast.success('Password updated successfully!');
      reset();
      
      // Call onSuccess callback if provided
      if (onSuccess) {
        onSuccess();
      }
    } catch (error: any) {
      toast.error(error?.response?.data?.message || error?.message || 'Failed to update password');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow dark:shadow-gray-600 rounded-lg">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        {/* <h2 className="text-lg font-medium text-gray-900 dark:text-white">Update Password</h2> */}
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Change your account password to keep your account secure
        </p>
      </div>
      
      <div className="px-6 py-4">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label htmlFor="currentPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Current Password
            </label>
            <input
              id="currentPassword"
              type="password"
              {...register('currentPassword')}
              className={`mt-1 w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 ${
                errors.currentPassword ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="Enter your current password"
            />
            {errors.currentPassword && (
              <p className="mt-1 text-sm text-red-600">{errors.currentPassword.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              New Password
            </label>
            <input
              id="newPassword"
              type="password"
              {...register('newPassword')}
              className={`mt-1 w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 ${
                errors.newPassword ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="Enter your new password"
            />
            {errors.newPassword && (
              <p className="mt-1 text-sm text-red-600">{errors.newPassword.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Confirm New Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              {...register('confirmPassword')}
              className={`mt-1 w-full border rounded-md px-3 py-2 bg-white dark:bg-gray-700 ${
                errors.confirmPassword ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="Confirm your new password"
            />
            {errors.confirmPassword && (
              <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
            )}
          </div>


          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isSubmitting}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Updating...
                </>
              ) : (
                'Update Password'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

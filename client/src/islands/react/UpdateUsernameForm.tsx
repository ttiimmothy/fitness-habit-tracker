import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import toast from 'react-hot-toast';
import { updateUsernameSchema, type UpdateUsernameFormData } from '../../schemas/authSchemas';
import { useUpdateProfile } from '../../hooks/useAuth';

interface UpdateUsernameFormProps {
  currentName: string;
  onSuccess?: () => void;
}

export default function UpdateUsernameForm({ currentName, onSuccess }: UpdateUsernameFormProps) {
  const updateProfileMutation = useUpdateProfile();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<UpdateUsernameFormData>({
    resolver: zodResolver(updateUsernameSchema),
    defaultValues: {
      name: currentName,
    },
  });

  const onSubmit = async (data: UpdateUsernameFormData) => {
    try {
      await updateProfileMutation.mutateAsync(data);
      toast.success('Username updated successfully!');
      reset();
      
      // Call onSuccess callback if provided
      if (onSuccess) {
        onSuccess();
      }
    } catch (error: any) {
      toast.error(error?.response?.data?.message || error?.message || 'Failed to update username');
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow dark:shadow-gray-600 rounded-lg">
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-600">
        {/* <h2 className="text-lg font-medium text-gray-900 dark:text-white">Update Username</h2> */}
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Change your display name that appears throughout the application
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="px-6 py-4 space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Full Name
          </label>
          <input
            {...register('name')}
            type="text"
            id="name"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 dark:text-white"
            placeholder="Enter your full name"
          />
          {errors.name && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.name.message}</p>
          )}
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Updating...' : 'Update Username'}
          </button>
        </div>
      </form>
    </div>
  );
}

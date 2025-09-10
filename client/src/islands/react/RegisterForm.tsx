import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import toast from 'react-hot-toast';
import { useRegister } from '../../hooks/useAuth';
import { registerSchema, type RegisterFormData } from '../../schemas/authSchemas';

export default function RegisterForm() {
  const registerMutation = useRegister();
  
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = (data: RegisterFormData) => {
    registerMutation.mutate(
      {
        name: data.name,
        email: data.email,
        password: data.password,
      },
      {
        onSuccess: () => {
          toast.success('Registration successful!');
          window.location.href = '/';
        },
        onError: (error: any) => {
          toast.error(error?.response?.data?.message || error?.message || 'Registration failed');
        },
      }
    );
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="block">
        <label htmlFor="name" className="text-sm font-medium">
          Full Name
        </label>
        <input
          id="name"
          type="text"
          {...register('name')}
          className={`mt-1 w-full border rounded px-3 py-2 bg-white dark:bg-neutral-800 ${
            errors.name ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
          }`}
          placeholder="Enter your full name"
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
        )}
      </div>
      
      <div className="block">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className={`mt-1 w-full border rounded px-3 py-2 bg-white dark:bg-neutral-800 ${
            errors.email ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
          }`}
          placeholder="Enter your email"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>
      
      <div className="block">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className={`mt-1 w-full border rounded px-3 py-2 bg-white dark:bg-neutral-800 ${
            errors.password ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
          }`}
          placeholder="Create a password"
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>
      
      <div className="block">
        <label htmlFor="confirmPassword" className="text-sm font-medium">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
          className={`mt-1 w-full border rounded px-3 py-2 bg-white dark:bg-neutral-800 ${
            errors.confirmPassword ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
          }`}
          placeholder="Confirm your password"
        />
        {errors.confirmPassword && (
          <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
        )}
      </div>
      
      {registerMutation.error && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded">
          <p className="text-sm text-red-600">
            {registerMutation.error?.response?.data?.message || 
             registerMutation.error?.message || 
             'Registration failed'}
          </p>
        </div>
      )}
      
      <button 
        type="submit"
        disabled={registerMutation.isPending || isSubmitting} 
        className="w-full bg-blue-600 text-white rounded py-2 disabled:opacity-70 hover:bg-blue-700 transition-colors font-medium"
      >
        {registerMutation.isPending || isSubmitting ? 'Creating account…' : 'Create Account'}
      </button>
      
      <div className="text-center">
        <p className="text-sm opacity-70">
          Already have an account?{' '}
          <a href="/login" className="text-blue-600 hover:underline font-medium">
            Sign in
          </a>
        </p>
      </div>
    </form>
  );
}

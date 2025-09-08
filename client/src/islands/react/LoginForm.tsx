import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useLogin } from '../../hooks/useAuth';
import { loginSchema, type LoginFormData } from '../../schemas/authSchemas';

export default function LoginForm() {
  const loginMutation = useLogin();
  
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: 'demo@example.com',
      password: 'Demo123!',
    },
  });

  const onSubmit = (data: LoginFormData) => {
    loginMutation.mutate(data, {
      onSuccess: () => {
        window.location.href = '/dashboard';
      },
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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
          placeholder="Enter your password"
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>

      {loginMutation.error && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded">
          <p className="text-sm text-red-600">
            {loginMutation.error?.response?.data?.message || 
             loginMutation.error?.message || 
             'Login failed'}
          </p>
        </div>
      )}

      <button 
        type="submit"
        disabled={loginMutation.isPending || isSubmitting} 
        className="w-full bg-blue-600 text-white rounded py-2 disabled:opacity-70 hover:bg-blue-700 transition-colors font-medium"
      >
        {loginMutation.isPending || isSubmitting ? 'Signing in…' : 'Sign in'}
      </button>
      
      <div className="text-center">
        <p className="text-sm opacity-70">
          Don't have an account?{' '}
          <a href="/register" className="text-blue-600 hover:underline font-medium">
            Create one
          </a>
        </p>
      </div>
    </form>
  );
}



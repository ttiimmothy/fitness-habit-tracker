import { z } from 'zod';

export const createHabitSchema = z.object({
  title: z
    .string()
    .min(1, 'Habit title is required')
    .min(2, 'Habit title must be at least 2 characters')
    .max(100, 'Habit title must be less than 100 characters'),
  description: z
    .string()
    .max(500, 'Description must be less than 500 characters')
    .optional(),
  frequency: z
    .enum(['daily', 'weekly', 'monthly'], {
      errorMap: () => ({ message: 'Please select a valid frequency' }),
    }),
  target: z
    .number()
    .min(1, 'Target must be at least 1')
    .max(100, 'Target must be less than 100'),
  category: z
    .string()
    .min(1, 'Category is required')
    .max(50, 'Category must be less than 50 characters'),
  // color: z
  //   .string()
  //   .regex(/^#[0-9A-F]{6}$/i, 'Please select a valid color')
  //   .optional(),
});

export type CreateHabitFormData = z.infer<typeof createHabitSchema>;

export const updateHabitSchema = z.object({
  title: z
    .string()
    .min(1, 'Habit title is required')
    .min(2, 'Habit title must be at least 2 characters')
    .max(100, 'Habit title must be less than 100 characters'),
  description: z
    .string()
    .max(500, 'Description must be less than 500 characters')
    .optional(),
  target: z
    .number()
    .min(1, 'Target must be at least 1')
    .max(100, 'Target must be less than 100'),
  category: z
    .string()
    .min(1, 'Category is required')
    .max(50, 'Category must be less than 50 characters'),
  // color: z
  //   .string()
  //   .regex(/^#[0-9A-F]{6}$/i, 'Please select a valid color')
  //   .optional(),
});

export type UpdateHabitFormData = z.infer<typeof updateHabitSchema>;

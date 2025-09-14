import { z } from 'zod';

// Badge status enum
export const BadgeStatus = z.enum(['earned', 'in_progress', 'locked']);
export type BadgeStatus = z.infer<typeof BadgeStatus>;

// Badge category enum
export const BadgeCategoryEnum = z.enum(['first_steps', 'consistency', "special_achievements", "wellness", 'fitness', 'social']);
export type BadgeCategoryEnum = z.infer<typeof BadgeCategoryEnum>;

// Individual badge schema
export const BadgeSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  category: BadgeCategoryEnum,
  icon_url: z.string().optional(),
  emoji: z.string().optional(),
  status: BadgeStatus,
  progress: z.object({
    current: z.number(),
    target: z.number(),
  }).optional(),
  earned_at: z.string().optional(), // ISO date string
  requirements: z.string().optional(), // Human readable requirements
});

// Badge category schema
export const BadgeCategorySchema = z.object({
  id: BadgeCategoryEnum,
  name: z.string(),
  emoji: z.string(),
  badges: z.array(BadgeSchema),
});

// Badges response schema
export const BadgesResponseSchema = z.object({
  categories: z.array(BadgeCategorySchema),
  total_badges: z.number(),
  earned_badges: z.number(),
  completion_percentage: z.number(),
});

// Type inference from schemas
export type Badge = z.infer<typeof BadgeSchema>;
export type BadgeCategory = z.infer<typeof BadgeCategorySchema>;
export type BadgesResponse = z.infer<typeof BadgesResponseSchema>;

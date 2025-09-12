import { create, StateCreator } from 'zustand';
import { devtools, persist, createJSONStorage } from 'zustand/middleware';
import { Habit } from '../hooks/useHabits';

type HabitState = {
  selectedHabit: Habit | null;
  setSelectedHabit: (habit: Habit | null) => void;
  clearSelectedHabit: () => void;
};

export const habitStoreCreate: StateCreator<HabitState, [], [], HabitState> = (set) => ({
  selectedHabit: null,
  setSelectedHabit: (habit) => set({ selectedHabit: habit }),
  clearSelectedHabit: () => set({ selectedHabit: null }),
});

export const useHabitStore = create<HabitState>()(
  // persist(
    devtools(
      habitStoreCreate,
      { name: "HabitStore" }
    ),
  //   {
  //     name: 'habitStore-storage',
  //     storage: createJSONStorage(() => localStorage),
  //     partialize: (state: HabitState): Partial<HabitState> => ({
  //       selectedHabit: state.selectedHabit
  //     })
  //   },
  // ),
);

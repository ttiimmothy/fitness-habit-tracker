import { create, StateCreator } from 'zustand';
import { devtools, persist, createJSONStorage } from 'zustand/middleware';
import {api} from "../lib/api";

export type User = { 
  id: string; 
  email: string; 
  name?: string | null; 
  avatar_url?: string | null;
  provider?: 'google' | 'email' | null;
  has_password?: boolean;
};

type AuthState = {
  user: User | null;
  setAuth: (u: User|null) => void;
  logout: () => Promise<void>;
};

// set, get order is important
export const authStoreCreate: StateCreator<AuthState, [], [], AuthState> = (set, get) => ({
  user: null,
  setAuth: (u) => set({user: u}),
  logout: async () => {
    const res = await api.post("/logout")
    const result = res.data
    if (result.message) {
      set( { user: null })
    }
  }
})

export const useAuthStore = create<AuthState>()(
  // persist(
    devtools(
      authStoreCreate,
      {name: "AuthStore"}
    ),
  //   { 
  //     name: 'authStore-storage',
  //     storage: createJSONStorage(() => localStorage),
  //     partialize: (state: AuthState):Partial<AuthState> => ({
  //       user: state.user
  //     })
  //   },
  // ),
);
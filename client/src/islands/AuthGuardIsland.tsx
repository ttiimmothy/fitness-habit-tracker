import { PersistQueryProvider } from "./react/PersistQueryProvider";
import {AuthGuard} from "./react/AuthGuard";
import React from "react";

export const AuthGuardIsland = ({children}: {children: React.ReactNode}) => {
  return (
    <PersistQueryProvider>
      <AuthGuard>{children}</AuthGuard>
    </PersistQueryProvider>
  );
};
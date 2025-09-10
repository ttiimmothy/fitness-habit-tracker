import { PersistQueryProvider } from "./react/PersistQueryProvider";
import AuthCheck from "./react/AuthCheck";
import React from "react";

export const AuthCheckIsland = ({children}: {children: React.ReactNode}) => {
  return (
    <PersistQueryProvider>
      <AuthCheck>{children}</AuthCheck>
    </PersistQueryProvider>
  );
};
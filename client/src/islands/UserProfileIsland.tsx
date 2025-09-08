import { PersistQueryProvider } from "./react/PersistQueryProvider";
import UserProfile from "./react/UserProfile";
import React from "react";

export const UserProfileIsland = () => {
  return (
    <PersistQueryProvider>
      <UserProfile />
    </PersistQueryProvider>
  );
};
import { PersistQueryProvider } from "./react/PersistQueryProvider";
import UserProfile from "./react/UserProfile";

export const UserProfileIsland = () => {
  return (
    <PersistQueryProvider>
      <UserProfile />
    </PersistQueryProvider>
  );
};
import { QueryProvider } from "../providers/QueryProvider";
import {UserProfile} from "./react/UserProfile";

export const UserProfileIsland = () => {
  return (
    <QueryProvider>
      <UserProfile />
    </QueryProvider>
  );
};
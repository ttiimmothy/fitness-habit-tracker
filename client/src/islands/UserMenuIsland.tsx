import { QueryProvider } from "../providers/QueryProvider";
import {UserMenu} from "./react/UserMenu";

export const UserMenuIsland = () => {
  return (
    <QueryProvider>
      <UserMenu/>
    </QueryProvider>
  )
}
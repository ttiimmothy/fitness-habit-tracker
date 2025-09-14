import { QueryProvider } from "../providers/QueryProvider";
import {AccountAction} from "./react/AccountAction";

export const AccountActionIsland = () => {
  return (
    <QueryProvider>
      <AccountAction />
    </QueryProvider>
  );
};
import { PersistQueryProvider } from "./react/PersistQueryProvider";
import {AuthGuard} from "./react/AuthGuard";

export const AuthGuardIsland = ({children}: {children: React.ReactNode}) => {
  return (
    <PersistQueryProvider>
      <AuthGuard>{children}</AuthGuard>
    </PersistQueryProvider>
  );
};
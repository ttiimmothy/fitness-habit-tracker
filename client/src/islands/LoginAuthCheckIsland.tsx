import { PersistQueryProvider } from "./react/PersistQueryProvider";
import {LoginAuthCheck} from "./react/LoginAuthCheck";

export const AuthCheckIsland = ({children}: {children: React.ReactNode}) => {
  return (
    <PersistQueryProvider>
      <LoginAuthCheck>{children}</LoginAuthCheck>
    </PersistQueryProvider>
  );
};
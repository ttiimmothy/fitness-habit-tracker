import { QueryProvider } from "../providers/QueryProvider";
import {GoogleLoginButton} from "./react/GoogleLoginButton";

export const GoogleLoginButtonIsland = () => {
  return (
    <QueryProvider>
      <GoogleLoginButton/>
    </QueryProvider>
  );
};
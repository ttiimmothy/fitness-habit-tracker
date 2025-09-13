import { QueryProvider } from "../providers/QueryProvider";
import {LoginForm} from "./react/LoginForm";

export const LoginFormIsland = () => {
  return (
    <QueryProvider>
      <LoginForm/>
    </QueryProvider>
  )
}
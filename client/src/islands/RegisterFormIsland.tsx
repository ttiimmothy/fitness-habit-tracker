import { QueryProvider } from "../providers/QueryProvider";
import {RegisterForm} from "./react/RegisterForm";

export const RegisterFormIsland = () => {
  return (
    <QueryProvider>
      <RegisterForm/>
    </QueryProvider>
  )
}
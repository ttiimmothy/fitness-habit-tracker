import {PersistQueryProvider} from "./react/PersistQueryProvider"
import LoginForm from "./react/LoginForm";

export const LoginFormIsland = () => {
  return (
    <PersistQueryProvider>
      <LoginForm/>
    </PersistQueryProvider>
  )
}
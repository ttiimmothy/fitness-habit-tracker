import {PersistQueryProvider} from "./react/PersistQueryProvider"
import RegisterForm from "./react/RegisterForm";

export const RegisterFormIsland = () => {
  return (
    <PersistQueryProvider>
      <RegisterForm/>
    </PersistQueryProvider>
  )
}
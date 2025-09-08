import {PersistQueryProvider} from "./react/PersistQueryProvider"
import RegisterForm from "./react/RegisterForm";
import React from "react"

export const RegisterFormIsland = () => {
  return (
    <PersistQueryProvider>
      <RegisterForm/>
    </PersistQueryProvider>
  )
}
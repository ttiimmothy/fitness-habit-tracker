import {PersistQueryProvider} from "./react/PersistQueryProvider"
import LoginForm from "./react/LoginForm";
import React from "react"

export const LoginFormIsland = () => {
  return (
    <PersistQueryProvider>
      <LoginForm/>
    </PersistQueryProvider>
  )
}
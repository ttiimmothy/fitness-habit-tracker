import {PersistQueryProvider} from "./react/PersistQueryProvider"
import UserMenu from "./react/UserMenu";
import React from "react"

export const UserMenuIsland = () => {
  return (
    <PersistQueryProvider>
      <UserMenu/>
    </PersistQueryProvider>
  )
}
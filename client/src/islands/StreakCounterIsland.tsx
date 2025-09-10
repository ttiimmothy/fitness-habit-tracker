import {PersistQueryProvider} from "./react/PersistQueryProvider"
import StreakCounter from "./react/StreakCounter";
import React from "react"

export const StreakCounterIsland = () => {
  return (
    <PersistQueryProvider>
      <StreakCounter/>
    </PersistQueryProvider>
  )
}
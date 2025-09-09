import {PersistQueryProvider} from "./react/PersistQueryProvider"
import HabitCard from "./react/HabitCard";
import React from "react"

export const HabitCardIsland = () => {
  return (
    <PersistQueryProvider>
      <HabitCard/>
    </PersistQueryProvider>
  )
}
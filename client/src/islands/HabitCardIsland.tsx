import {PersistQueryProvider} from "./react/PersistQueryProvider"
import HabitCard from "./react/HabitCard";

export const HabitCardIsland = () => {
  return (
    <PersistQueryProvider>
      <HabitCard/>
    </PersistQueryProvider>
  )
}
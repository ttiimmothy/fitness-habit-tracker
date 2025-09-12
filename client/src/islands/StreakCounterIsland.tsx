import {PersistQueryProvider} from "./react/PersistQueryProvider"
import StreakCounter from "./react/StreakCounter";

export const StreakCounterIsland = () => {
  return (
    <PersistQueryProvider>
      <StreakCounter/>
    </PersistQueryProvider>
  )
}
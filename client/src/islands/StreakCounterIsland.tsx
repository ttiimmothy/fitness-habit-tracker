import { QueryProvider } from "../providers/QueryProvider";
import {StreakCounter} from "./react/StreakCounter";

export const StreakCounterIsland = () => {
  return (
    <QueryProvider>
      <StreakCounter/>
    </QueryProvider>
  )
}
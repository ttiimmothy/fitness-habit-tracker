import { QueryProvider } from "../providers/QueryProvider";
import {HabitCard} from "./react/HabitCard";

export const HabitCardIsland = () => {
  return (
    <QueryProvider>
      <HabitCard/>
    </QueryProvider>
  )
}
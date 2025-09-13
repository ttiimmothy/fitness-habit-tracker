import { QueryProvider } from "../providers/QueryProvider";
import {IndividualHabitChart} from './react/IndividualHabitChart';

export const IndividualHabitChartIsland = () => {
  return (
    <QueryProvider>
      <IndividualHabitChart />
    </QueryProvider>
  );
}

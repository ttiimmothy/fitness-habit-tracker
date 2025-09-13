import { QueryProvider } from "../providers/QueryProvider";
import {IndividualHabitQuickLog} from './react/IndividualHabitQuickLog';

export const IndividualHabitQuickLogIsland = () => {
  return (
    <QueryProvider>
      <IndividualHabitQuickLog />
    </QueryProvider>
  );
}

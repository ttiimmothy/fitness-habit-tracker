import {PersistQueryProvider} from './react/PersistQueryProvider';
import IndividualHabitChart from './react/IndividualHabitChart';

export default function IndividualHabitChartIsland() {
  return (
    <PersistQueryProvider>
      <IndividualHabitChart />
    </PersistQueryProvider>
  );
}

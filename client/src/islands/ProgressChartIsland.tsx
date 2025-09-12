import { PersistQueryProvider } from "./react/PersistQueryProvider";
import ProgressChart from "./react/ProgressChart";

export const ProgressChartIsland = () => {
  return (
    <PersistQueryProvider>
      <ProgressChart />
    </PersistQueryProvider>
  );
};
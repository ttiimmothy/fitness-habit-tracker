import { QueryProvider } from "../providers/QueryProvider";
import {ProgressChart} from "./react/ProgressChart";

export const ProgressChartIsland = () => {
  return (
    <QueryProvider>
      <ProgressChart />
    </QueryProvider>
  );
};
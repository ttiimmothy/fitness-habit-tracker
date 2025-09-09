import { PersistQueryProvider } from "./react/PersistQueryProvider";
import ProgressChart from "./react/ProgressChart";
import React from "react";

export const ProgressChartIsland = () => {
  return (
    <PersistQueryProvider>
      <ProgressChart />
    </PersistQueryProvider>
  );
};
import { QueryProvider } from "../providers/QueryProvider";
import { BadgeProgressSummary } from './react/BadgeProgressSummary';

export const BadgeProgressSummaryIsland = () => {
  return (
    <QueryProvider>
      <BadgeProgressSummary />
    </QueryProvider>
  );
};

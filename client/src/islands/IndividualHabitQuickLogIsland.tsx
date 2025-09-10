import React from 'react';
import { PersistQueryProvider } from './react/PersistQueryProvider';
import IndividualHabitQuickLog from './react/IndividualHabitQuickLog';

export default function IndividualHabitQuickLogIsland() {
  return (
    <PersistQueryProvider>
      <IndividualHabitQuickLog />
    </PersistQueryProvider>
  );
}

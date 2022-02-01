interface Hierarchy {
  goal: string;
  criteria: Criterion[];
}

interface Criterion {
  title: string;
  subCriteria: Criterion[];
}

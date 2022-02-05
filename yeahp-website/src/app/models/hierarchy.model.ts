export interface Hierarchy {
  goal: string;
  criteria: Criterion[];
}

export interface Criterion {
  title: string;
  subCriteria: Criterion[];
}

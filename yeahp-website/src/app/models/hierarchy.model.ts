export interface Hierarchy {
  goal: string;
  criteria: string[];
  dependencies: Array<[string, string]>;
}

/* export interface Hierarchy {
  goal: string;
  criteria: Criterion[];
}

export interface Criterion {
  title: string;
  subCriteria: Criterion[];
} */

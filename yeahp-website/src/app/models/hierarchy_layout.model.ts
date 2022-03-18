export interface HierarchyLayout {
  y_coordinates: Array<[string, number]>;
  class_by_depth: string[][];
}

export interface HierarchyLayoutPayload {
  root: string;
  dependencies: Array<[string, string]>;
}

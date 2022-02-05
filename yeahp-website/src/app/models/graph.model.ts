export class Graph<T> {
  private _nodes: string[] = [];
  private _edges: Array<[string, string]> = [];
  private _nodeAssets: Map<string, T> = new Map<string, T>();

  constructor() {}

  addNode(nodeLabel: string, asset?: T): void {
    if (this._nodes.includes(nodeLabel)) {
      throw `Cannot create node '${nodeLabel}' as it already exists`;
    }
    this._nodes.push(nodeLabel);

    // Stores asset if any
    if (asset != undefined) {
      this._nodeAssets.set(nodeLabel, asset);
    }
  }

  addEdge(fromLabel: string, toLabel: string): void {
    if (!(this._nodes.includes(fromLabel) && this._nodes.includes(toLabel))) {
      throw `Cannot create edge (${fromLabel}, ${toLabel}): some nodes does not exist`;
    }
    this._edges.push([fromLabel, toLabel]);
  }
}
